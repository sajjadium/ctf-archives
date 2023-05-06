#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import os
import sys
import time
import base64
import signal
import random
import string
import uuid

S = string.letters+string.digits+'_'


def handler(signum, frame):
    print('time up!')
    exit(0)

def generate_filename():
    a = '/tmp/'
    a += str(uuid.uuid1())
    a += '.js'
    return a

def banner():
    print("___________                ____         ____.                       ")
    print("\__    ___/___   _____    /  _ \       |    | __________________ ___.__.")
    print("  |    | /  _ \ /     \   >  _ </\     |    |/ __ \_  __ \_  __ <   |  |")
    print("  |    |(  <_> )  Y Y  \ /  <_\ \/ /\__|    \  ___/|  | \/|  | \/\___  |")
    print("  |____| \____/|__|_|  / \_____\ \ \________|\___  >__|   |__|   / ____|")
    print("                     \/         \/               \/              \/     ")
    print("                                                                 Nu1L   ")


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(30)
    try:
        inputs = ""
        banner()
        print("Please input your base64encode exploit:")
        while True:
            line = sys.stdin.readline()
            line = line.strip()
            if line == "EOF":
                break
            inputs = inputs + line
        inputs = base64.b64decode(inputs)
        if len(inputs) > 2**12:
            print('Too big')
            sys.exit(0)
        try:
            filename = generate_filename()
            with open(filename, 'wb') as tmp:
                size = len(inputs)
                cur_idx = 0
                while(cur_idx < size):
                    tmp.write(inputs[cur_idx])
                    cur_idx += 1

            os.system("/jerry %s" % filename)
            sys.exit(0)
        except Exception as ex:
            print('error:%s' % ex)
            sys.exit(0)
        finally:
            if os.path.exists(filename):
                os.remove(filename)
            sys.exit(0)
    except Exception as ex:
        print('error:%s' % ex)
        sys.exit(0)
