#!/usr/bin/env python3
import os
import random
import shutil
import string

ctable = string.ascii_letters + string.digits
rndstr = lambda n: ''.join([random.choice(ctable) for i in range(n)])

PATH = '/tmp/babyauth_' + rndstr(16)
USERNAME = 'admin'
PASSWORD = rndstr(16)

if __name__ == '__main__':
    # Setup
    os.makedirs(PATH, exist_ok=True)
    with open(f'{PATH}/username', 'w') as f:
        f.write(USERNAME)
    with open(f'{PATH}/password', 'w') as f:
        f.write(PASSWORD)

    # Prove your exploit is stable
    for ROUND in range(5):
        # Authentication
        if os.system(f'./auth {PATH}') != 0:
            shutil.rmtree(PATH)
            exit(0)
        print(f"[+] {ROUND+1}/5: OK", flush=True)

    # Delicious Fruit
    with open("/flag", "r") as f:
        print(f.read())

    # Cleanup
    shutil.rmtree(PATH)
