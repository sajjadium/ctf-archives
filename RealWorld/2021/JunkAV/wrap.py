import subprocess
from hashlib import sha256
import string
import random
import base64
import os
import signal
import sys
import time

MAX_FILE_SIZE = 1024 * 1024 * 8
WORK_PATH     = b'/home/ctf/check/'

def rand_str(length):
    return ''.join(random.choice(string.ascii_letters) for i in range(length)).encode('latin1')

def get_choice():

    choic = input('> Continue (Y/N)\n')
    if choic == "N" or choic == "n":
        exit(0)
    elif choic == "Y" or choic == 'y':
        return 
    else:
        exit(0)

def get_file():
    data = input('> Upload the file (base64)\n')
    try:
        data = base64.b64decode(data)
        if (len(data) > MAX_FILE_SIZE):
            raise Exception("The uploaded file is too large (MAX: {:#x}".format(MAX_FILE_SIZE))
        name = WORK_PATH + teamtoken.encode('latin1') + b'_'  + str(int(time.time())).encode('latin1') +  rand_str(20)
        with open(name, 'wb') as f:
            f.write(data)
    except Exception as e :
        print(e)
        exit(1)
    return name

def run_junkav():
    get_choice()
    fname = get_file().decode('latin1')
    subprocess.run(['/home/ctf/junkav','/home/ctf/rules/all-yara.yar', fname],  stderr=subprocess.STDOUT, timeout=3)
    return 


if __name__  == '__main__':
    if len(sys.argv) == 2:
        global teamtoken
        teamtoken = sys.argv[1]
        signal.alarm(50)
        try:
            print("You have 10 chances to check your file\n")
            for i in range(10):
                run_junkav()
        except Exception as e :
            print(e)
