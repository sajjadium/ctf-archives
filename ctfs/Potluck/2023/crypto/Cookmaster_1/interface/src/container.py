import subprocess
import os
import docker


def create_can_interface(team_id):
    client = docker.from_env()
    
    containers =client.containers.list(filters={"name": f"team_{team_id}-heater"})
    if len(containers) != 1:
        raise Exception("Problem with container filtering")
    container = containers[0]
    pid = container.attrs['State']['Pid']
    if pid == 0:
        raise Exception("Container not running?")
    print(pid)
    proc = subprocess.run(['./create_canbridge.sh', f'c{team_id}', str(pid) ], capture_output=True)
    print(proc.stdout)
    print(proc.stderr)



def container_state(team_id, cmd):
    os.environ['COMPOSE_PROJECT_NAME'] = f'team_{team_id}'
    os.environ['TEAM_ID'] = str(team_id)
    os.environ['COMPOSE_FILE'] = '../cookmaster/docker-compose.yml'

    if cmd == 'start':
        subprocess.run(['docker', 'compose', 'up', '-d', '--build'], capture_output=True)
        create_can_interface(team_id)
    if cmd == 'stop':
        subprocess.run(['docker', 'compose', 'down'], capture_output=True)



if __name__ == "__main__":
    import sys
    team_id = sys.argv[2]
    cmd = sys.argv[1] if len(sys.argv) > 1 else "start" 
    container_state(team_id, cmd)
