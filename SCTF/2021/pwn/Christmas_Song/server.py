#! /usr/bin/python3
import os
import subprocess
import sys
import uuid

def socket_print(string):
    print("=====", string, flush=True)


def get_user_input():
    socket_print("Enter partial source for edge compute app (EOF to finish):")
    user_input = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "EOF":
            break
        user_input.append(line)
    socket_print("Input accepted!")
    return user_input


def write_to_slang(contents, filename):
    socket_print("Writing source to disk...")

    with open("{}.slang".format(filename), 'w') as fd:
        fd.write('\n'.join(contents))

def run_challenge(filename):
    socket_print("Testing edge compute app...")
    try: 
        result = subprocess.run("/home/ctf/Christmas_Song -r {}.slang".format(filename), shell=True, timeout=1)
    except subprocess.TimeoutExpired:
        pass
    clean(filename);
    socket_print("Test complete!")

def get_filename():
    return "/tmp/{}".format(uuid.uuid4().hex)

def clean(filename):
    result = subprocess.run("rm {}.*".format(filename), shell=True, timeout=10)

def main():
    user_input = get_user_input()
    if (len(user_input) == 0):
        exit()
    filename = get_filename()
    write_to_slang(user_input, filename)
    run_challenge(filename)


if __name__ == "__main__":
    main()
