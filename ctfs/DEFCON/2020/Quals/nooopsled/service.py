#!/usr/bin/env python3

import subprocess
import tempfile
import fuckpy3 #pylint:disable=unused-import
import os

ARCHITECTURES = { "aarch64", "riscv64" }
THRESHOLD = int(os.environ.get('THRESHOLD', 1000))

def main():
    print("Historically, shellcode was judged by what it could do. This outmoded")
    print("way of thought was cast down in the revolution of August 2018, and a")
    print("new Order was established: shellcode would be judged by how widely")
    print("applicable it was to different machines. In 2019, this Order was refined:")
    print("like all things, shellcode would be measured by how resilient it was to")
    print("corruption.")
    print("")
    print("The time for change has come again. Shellcode must be ready for anything,")
    print("regardless of where it's executed and *from when* it's executed. This is")
    print("not easy, but the Order is kind. You will have some time to perfect your")
    print("shellcoding skills.")
    print("")
    print(f"The Order will currently accept {THRESHOLD} failures. You may choose the")
    print("architecture of the future: aarch64 or riscv64?")
    arch = input("What is your choice? ")
    assert arch in ARCHITECTURES, "The Order has no use for this architecture."
    shellcode = input("Input your shellcode (in hex): ").unhex()
    assert len(shellcode) == 1024, "The order demands perfectly-sized 1KB shellcode."

    fails = 0
    for offset in range(1024):
        flag = os.urandom(16).hex().bytes()
        shifted_code = shellcode[offset:].ljust(1024, b"\x00")
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chmod(tmpdir, 0o777)
            with open(f"{tmpdir}/flag", "wb") as flagfile:
                flagfile.write(flag)
            out,_ = subprocess.Popen([
                f"{os.path.dirname(__file__)}/shuffler", "10",
                f"/usr/bin/qemu-{arch}", "-L", f"/usr/{arch}-linux-gnu/",
                f"{os.path.dirname(__file__)}/launcher-{arch}"
            ], cwd=tmpdir, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate(shifted_code, timeout=20)
            if flag in out:
                print(f"Success with offset {offset}!")
            else:
                fails += 1
                print(f"Failure with offset {offset} (cumulative: {fails})!")

    if fails <= THRESHOLD:
        print("The Order is pleased with your shellcode.")
        print(open(f"{os.path.dirname(__file__)}/flag").read())
    else:
        print("The Order is displeased with your shellcode.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e: #pylint:disable=broad-except
        print(f"Something went wrong: {e}")
