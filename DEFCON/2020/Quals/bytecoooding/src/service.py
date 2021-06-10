#!/usr/bin/env python3

import os
import random
import shutil
import signal
import string
import subprocess
import sys
import tempfile

THRESHOLD = int(os.environ.get('THRESHOLD', 1000))

PLATFORMS = ["jvm", "python3", "python2", "ruby", "lua", "nodejs", "ocaml", "elisp"]

FLAG_LOCATION = '/flag'
DEBUG = False

def get_platforms():
    to_return = set()
    print(f"Choose the platforms ({' '.join(PLATFORMS)}) you want to run your bytecode against")
    done = False
    while not done:
        choice = input("> ").strip()
        if choice in PLATFORMS:
            to_return.add(choice)
        else:
            done = True
    return to_return

def input_bytecode(limit=4096):
    print("Bytecode: ")
    d = sys.stdin.buffer.read1(limit)
    if len(d) == 0:
        sys.exit(0)
    return d

def grade_platform(bytecode, platform_test, preamble_loc):

    with tempfile.TemporaryDirectory() as tmpdir:

        uid = random.randint(2000, 30000)
        os.chown(tmpdir, uid, uid)
        os.chmod(tmpdir, 0o700)

        # create this specific flag
        flag = "OOO" + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        flag = flag.encode('utf-8')
        flag_loc = f"{tmpdir}/flag"
        with open(flag_loc, 'wb') as flag_file:
            flag_file.write(flag)

        os.chown(flag_loc, uid, uid)
        os.chmod(flag_loc, 0o400)

        # copy bytecode to a file
        bytecode_loc = f"{tmpdir}/bytecode"
        with open(bytecode_loc, 'wb') as bytecode_file:
            with open(preamble_loc, 'rb') as preamble:
                bytecode_file.write(preamble.read())

            bytecode_file.write(bytecode)

        os.chown(bytecode_loc, uid, uid)
        os.chmod(bytecode_loc, 0o400)

        run_loc = f"{tmpdir}/run"
        shutil.copyfile(platform_test, run_loc)
        os.chown(run_loc, uid, uid)
        os.chmod(run_loc, 0o550)

        os.chdir(tmpdir)
        
        # execute platform grading script
        result = subprocess.run(["/usr/bin/sudo", "-u", f"#{uid}", "-g", f"#{uid}", run_loc],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        if DEBUG:
            print(f"{result.stdout}\n{result.stderr}")
        # cleanup
        subprocess.run(["/usr/bin/sudo", "-u", f"#{uid}", "-g", f"#{uid}", "kill", "-9", "-1"])
        
        if result.returncode != 0:
            return 0

        # compare output to the flag
        return flag in result.stdout

def main():
    print("Shellcoding is so 👴👵")
    print("Let's go 😎 to the future")
    print("That's right, I'M TALKING BOUT BYTECODE!")
    print("")
    print(f"Let's see what you got. You'll only get the flag if you can do {THRESHOLD} platforms.")
    bytecode = input_bytecode()

    platforms_to_test = get_platforms()

    platform_path = os.path.dirname(os.path.realpath(__file__))

    num_correct = 0
    for p in sorted(list(platforms_to_test)):
        is_correct = grade_platform(bytecode, f"{platform_path}/platforms/{p}/run", f"{platform_path}/platforms/{p}/preamble")
        if is_correct:
            num_correct += 1
        else:
            break

    print(f"You got {num_correct} correct")
    if num_correct >= THRESHOLD:
        flag = open(FLAG_LOCATION, 'r').read()
        print(f"Great job! Flag: {flag}")
    else:
        print(f"Not quite there, still need to complete {THRESHOLD-num_correct} platforms")
        

def timeout_handler(signum, frame):
    print("Timeout")
    os.kill(os.getpid(), signal.SIGKILL)

if __name__ == '__main__':
    signal.alarm(240)
    signal.signal(signal.SIGALRM, timeout_handler)
    main()
