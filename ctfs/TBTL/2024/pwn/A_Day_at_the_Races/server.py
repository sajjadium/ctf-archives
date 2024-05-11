#!/usr/bin/python3

import base64
import hashlib
import io
import signal
import string
import subprocess
import sys
import time


REVIEWED_SOURCES = [
    "24bf297fff03c69f94e40da9ae9b39128c46b7fe", # fibonacci.c
    "55c53ce7bc99001f12027b9ebad14de0538f6a30", # primes.c
]


def slow_print(s, baud_rate=0.1):
    for letter in s:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(baud_rate)


def handler(_signum, _frame):
    slow_print("Time out!")
    exit(0)


def error(message):
    slow_print(message)
    exit(0)


def check_filename(filename):
    for c in filename:
        if not c in string.ascii_lowercase + ".":
            error("Invalid filename\n")


def check_compile_and_run(source_path):
    slow_print("Checking if the program is safe {} ...\n".format(source_path))
    hash = hashlib.sha1(open(source_path, 'rb').read()).hexdigest()
    if not hash in REVIEWED_SOURCES:
        error("The program you uploaded has not been reviewed yet.")
    exe_path = source_path + ".exe"
    slow_print("Compiling {} ...\n".format(source_path))
    subprocess.check_call(["/usr/bin/gcc", "-o", exe_path, source_path])
    slow_print("Running {} ...\n".format(exe_path))
    time_start = time.time()
    subprocess.check_call(exe_path)
    duration = time.time()-time_start
    slow_print("Duration {} s\n".format(duration))


def main():
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(300)

    slow_print("Let's see what kind of time your C program clocks today!\n")
    slow_print("Enter filename: ")
    filename = input()
    check_filename(filename)
    filepath = "./run/" + filename

    slow_print("Enter contents (base64): ")
    contents = input()
    try:
        data = base64.decode(io.StringIO(contents), open(filepath, 'wb'))
    except Exception as e:
        error("Error decoding contents ({}).\n".format(e))

    check_compile_and_run(filepath)
    slow_print("Bye!\n")


if __name__ == "__main__":
    main()
