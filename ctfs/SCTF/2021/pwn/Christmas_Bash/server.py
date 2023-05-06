#! /usr/bin/python3
import os
import subprocess
import sys
import uuid
import urllib.request

def socket_print(string):
    print("=====", string, flush=True)


def get_user_input(filename):
    socket_print("please input your flag url: ")
    url = input()
    urllib.request.urlretrieve(url,filename)
    socket_print("Okay, now I've got the file")


def run_challenge(filename):
    socket_print("Don't think I don't know what you're up to.")
    socket_print("You must be a little hack who just learned the Christmas song!")
    socket_print("Come let me test what you gave me!")
    result = subprocess.run("/home/ctf/Christmas_Bash -r {} < /dev/null".format(filename), shell=True)
    print(result)
    if (result == "hellow!"):
        socket_print("wow, that looks a bit unusual, I'll try to decompile it and see.")
        subprocess.run("/home/ctf/Christmas_Bash -r {} -d {} < /dev/null".format(filename, filename), shell=True)
    else:
        socket_print("Hahahahahahahahahahahahaha, indeed, you should also continue to learn Christmas songs!")
    clean(filename);

def get_filename():
    return "/tmp/{}.scom".format(uuid.uuid4().hex)

def clean(filename):
    result = subprocess.run("rm {}".format(filename), shell=True, timeout=10)

def main():
    filename = get_filename()
    get_user_input(filename)
    run_challenge(filename)


if __name__ == "__main__":
    main()
