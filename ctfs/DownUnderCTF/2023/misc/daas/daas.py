#!/usr/local/bin/python3.8

import subprocess
import sys
import tempfile
import base64

print("Welcome to my .pyc decompiler as a service!")
try:
   pyc = base64.b64decode(input('Enter your pyc (base64):\n'))
except:
   print('There was an error with your base64 :(')
   exit(1)

with tempfile.NamedTemporaryFile(suffix='.pyc') as sandbox:
    sandbox.write(pyc)
    sandbox.flush()
    pipes = subprocess.Popen(["/usr/local/bin/decompyle3", sandbox.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pipes.communicate()
    if pipes.returncode == 0 and len(stderr) == 0:
        print(stdout.decode())
    else:
        print(stderr.decode())
        print("There was an error in decompilation :(")
