import os
from pathlib import Path
import subprocess
import string
from typing import Optional


class MyException(Exception):
    pass


def compile(basename: str, src: bytes) -> Path:
    with open(f"/opt/transfer/{basename}.c", "wb") as f:
        f.write(src)

    cmd = f"/opt/jailyard/compile.sh {basename}"
    popen = subprocess.Popen(
        f'/opt/app/run_jail.sh /opt/app/jails/gcc.cfg "{cmd}"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        bufsize=0,
    )

    for s in popen.stdout:
        print(s, end="")

    popen.stdout.close()
    popen.wait()
    filepath = Path("/opt/transfer") / basename

    if not filepath.is_file():
        raise MyException("[-] Your code actually has to compile")

    return filepath


def solve_key(filepath: Path) -> Optional[str]:
    cmd = f"/usr/bin/python3 /opt/jailyard/solver.py {filepath}"
    popen = subprocess.Popen(
        f'/opt/app/run_jail.sh /opt/app/jails/angr.cfg "{cmd}"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        bufsize=0,
    )

    key = None
    for s in popen.stdout:
        print(s, end="")
        if s.startswith("[*] Key: "):
            key = s.lstrip("[*] Key: ").strip()

    popen.stdout.close()
    popen.wait()
    return key


def check_key(filepath: Path, key: str) -> bool:
    cmd = f"{filepath} {key}"
    popen = subprocess.Popen(
        f'/opt/app/run_jail.sh /opt/app/jails/bin.cfg "{cmd}"',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf-8",
        bufsize=0,
    )

    for s in popen.stdout:
        print(s, end="")

    popen.stdout.close()
    popen.wait()
    return popen.returncode == 0


def start(basename: str):
    print("[*] Write me a program that:")
    print("[*] - Takes 4 uppercase characters in argv")
    print("[*] - Verifies the 4 character key and returns 0 if correct")
    print("[*] - If I find the key, YOU LOSE")
    print("")
    print("[*] Enter your C code in hex:")
    src = bytes.fromhex(input())
    if len(src) > 2048:
        raise MyException("[-] Too long nitwit")

    print("[*] Compiling ...")
    filepath = compile(basename, src)

    print("[*] Solving (max 2 minutes) ...")
    key = solve_key(filepath)

    if key:
        print(f"[-] WoUlD yOu LoOk At ThIs KeY i FoUnD: {key}")
        raise MyException("[-] This code is WEAK SAUCE")
    else:
        print("[*] My solver couldn't find a key >:(")

    key = input("[*] Gimme ur key and I'll check it: ")
    if len(key.encode()) != 4:
        raise MyException("[-] The key needs to be 4 characters fool")
    if any(c not in string.ascii_uppercase for c in key):
        raise MyException("[-] The key can only contain UPPERCASE characters")

    success = check_key(filepath, key)
    if success:
        print("[*] WTF? YOUR KEY WORKS")
        print("[*] You are a crypto genius")
        flag = open("flag.txt").read().strip()
        print(f"[+] Here's your flag: {flag}")
    else:
        raise MyException("[-] ARE YOU KIDDING ME? THIS KEY DOESN'T EVEN WORK")


def main():
    basename = os.urandom(4).hex()
    try:
        start(basename)
    except MyException as e:
        print(e)

    try:
        os.remove(Path("/opt/transfer") / f"{basename}.c")
        os.remove(Path("/opt/transfer") / basename)
    except OSError:
        pass


if __name__ == "__main__":
    main()
