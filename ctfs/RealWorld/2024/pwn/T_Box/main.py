import sys
import subprocess
import pathlib
import argparse

work_dir = pathlib.Path(__file__).parent.absolute()
instance_dir = pathlib.Path("/var/run/tbox")


class CmdFailed(Exception):
    pass


def build_docker(name: str):
    cmd = ["docker", "build", "-t", name, work_dir / name]
    run_cmd(cmd)


def run_cmd(argv: list, cwd=work_dir) -> bytes:
    f = subprocess.run(argv, cwd=cwd, capture_output=True)
    if f.returncode != 0:
        raise CmdFailed(f"Command failed: {argv}: {f.stderr.decode()}")
    return f.stdout


def kill_docker(name: str):
    cmd = ["docker", "kill", name]
    try:
        run_cmd(cmd)
    except CmdFailed as e:
        print(e)


def attach_ns(pid: int, name: str):
    cmd = ["ip", "netns", "attach", name, str(pid)]
    run_cmd(cmd)


def delete_ns(name: str):
    cmd = ["ip", "netns", "delete", name]
    try:
        run_cmd(cmd)
    except CmdFailed as e:
        print(e)


def get_docker_pid(name: str):
    cmd = ["docker", "top", name]
    result = run_cmd(cmd)
    line = result.split(b"\n")[1]
    pid = line.split()[1]
    return int(pid)


def set_ns(name: str, cmdline: str):
    cmd = ["ip", "netns", "exec", name, "sh", "-c", cmdline]
    run_cmd(cmd)


def get_ssh_port(name: str):
    cmd = ["docker", "port", name, "22"]
    result = run_cmd(cmd)
    return int(result.split(b'\n')[0].split(b":")[1])


GATEBOX_CMD = '''
ip link add jumpbox type bridge
ip addr add dev jumpbox 10.233.1.1/24
ip link set jumpbox up

ip link add veth_jumpbox type veth peer vm
ip link set dev vm netns {jumpbox_name}
ip link set veth_jumpbox master jumpbox
ip link set veth_jumpbox up

ip link add flagbox type bridge
ip addr add dev flagbox 10.233.2.1/24
ip link set flagbox up

ip link add veth_flagbox type veth peer vm
ip link set dev vm netns {flagbox_name}
ip link set veth_flagbox master flagbox
ip link set veth_flagbox up


iptables -t nat -I POSTROUTING -o eth0 -j MASQUERADE
iptables -I FORWARD -i flagbox -o jumpbox -j DROP
iptables -I FORWARD -o flagbox -i jumpbox -j DROP
iptables -t nat -I PREROUTING -p tcp --dport 22 -j DNAT --to-destination 10.233.1.2:22
'''

JUMPBOX_CMD = '''
ip link set dev vm name eth0
ip addr add 10.233.1.2/24 dev eth0
ip link set dev eth0 up
ip route add 0.0.0.0/0 via 10.233.1.1 dev eth0
'''

FLAGBOX_CMD = '''
ip link set dev vm name eth0
ip addr add 10.233.2.2/24 dev eth0
ip link set dev eth0 up
ip route add 0.0.0.0/0 via 10.233.2.1 dev eth0
'''


def start(identifier: str):
    id_path = instance_dir / identifier
    if id_path.exists():
        print("Instance already exists")
        sys.exit(1)
    else:
        id_path.touch()

    # first start all containers
    jumpbox_name = f"jumpbox_{identifier}"
    flagbox_name = f"flagbox_{identifier}"
    gatebox_name = f"gatebox_{identifier}"

    cmd = ["docker", "run", "-d", "--rm", "--name", jumpbox_name, "--network", 'none', "--cap-add", "NET_RAW",
           "jumpbox"]
    run_cmd(cmd)

    # change password for jumpbox
    run_cmd(["docker", "exec", jumpbox_name, "sh", "-c", f"echo 'root:{identifier}' | chpasswd"])

    cmd = ["docker", "run", "-d", "--rm", "--name", flagbox_name, "--network", 'none', "flagbox"]
    run_cmd(cmd)

    cmd = ["docker", "run", "-d", "--rm", "--name", gatebox_name, "--network", "bridge", "-p", "22", "gatebox"]
    run_cmd(cmd)

    attach_ns(get_docker_pid(jumpbox_name), jumpbox_name)
    attach_ns(get_docker_pid(flagbox_name), flagbox_name)
    attach_ns(get_docker_pid(gatebox_name), gatebox_name)

    set_ns(gatebox_name, GATEBOX_CMD.format(jumpbox_name=jumpbox_name, flagbox_name=flagbox_name))
    set_ns(jumpbox_name, JUMPBOX_CMD)
    set_ns(flagbox_name, FLAGBOX_CMD)

    ssh_port = get_ssh_port(gatebox_name)
    print(f"ssh -p {ssh_port} root@127.0.0.1")


def cleanup(identifier):
    jumpbox_name = f"jumpbox_{identifier}"
    flagbox_name = f"flagbox_{identifier}"
    gatebox_name = f"gatebox_{identifier}"

    kill_docker(jumpbox_name)
    kill_docker(flagbox_name)
    kill_docker(gatebox_name)
    delete_ns(jumpbox_name)
    delete_ns(flagbox_name)
    delete_ns(gatebox_name)

    id_path = instance_dir / identifier
    id_path.unlink()


def init():
    instance_dir.mkdir(parents=True, exist_ok=True)
    cmd = ["docker", "version"]
    run_cmd(cmd)

    cmd = ["ip", 'a']
    run_cmd(cmd)

    # build docker image
    build_docker("jumpbox")
    build_docker("gatebox")
    build_docker("flagbox")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop", "init"])
    parser.add_argument("identifier", type=str, help="identifier for the challenge")

    arg = parser.parse_args()
    if arg.action == "stop":
        cleanup(arg.identifier)
    elif arg.action == "start":
        start(arg.identifier)
    elif arg.action == "init":
        init()
    else:
        print("Unknown command")
