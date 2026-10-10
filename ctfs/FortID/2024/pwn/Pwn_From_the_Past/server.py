#!/usr/bin/python3

import base64
import os
import shutil
import signal
import subprocess
import tempfile


def myprint(s):
    print(s, flush=True)


def handler(_signum, _frame):
    myprint("Time out!")
    exit(0)


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)

    myprint("Enter contents for INPUT.TXT (base64): ")
    contents = input()
    try:
        data = base64.b64decode(contents)
    except Exception as e:
        myprint("Error decoding contents ({}).\n".format(e))
        exit(0)

    tmp_dir = tempfile.mkdtemp(dir="./run")
    shutil.copy("flag.txt", os.path.join(tmp_dir, "FLAG.TXT"))
    shutil.copy("RUN.BAT", os.path.join(tmp_dir, "RUN.BAT"))
    shutil.copy("CHALL.EXE", os.path.join(tmp_dir, "CHALL.EXE"))
    input_filename = os.path.join(tmp_dir, "INPUT.TXT")  
    input_file = open(input_filename, "wb")
    input_file.write(data)
    input_file.close()

    cmd = ["/usr/bin/dosbox", "-c", f"MOUNT C {tmp_dir}", "-c", "C:\RUN.BAT"]
    env = {"SDL_VIDEODRIVER": "dummy"} # Supress dosbox GUI
    myprint(f"Running {' '.join(cmd)}")
    subprocess.check_output(cmd, env=env)

    try:
        output_filename = os.path.join(tmp_dir, "OUTPUT.TXT")  
        output_data = open(output_filename, "rb").read()
        myprint("Your OUTPUT.TXT: {}".format(base64.b64encode(output_data).decode()))
    except FileNotFoundError:
        myprint("Program did not produce OUTPUT.TXT")


if __name__ == "__main__":
    main()
