#!/usr/bin/env python3
import os
import base64
import random
import subprocess

random.seed(os.urandom(32))

# Enjoy the music :)
SALT_DICT=base64.b64decode(b'aHR0cHM6Ly95LnFxLmNvbS9uL3J5cXEvc29uZ0RldGFpbC8wMDAyOTJXNjJvODd3Rg==')

def generate_salts():
    num_salts=random.randint(1,16)
    return [bytes(random.choices(SALT_DICT,k=random.randint(16,32))) for _ in range(num_salts)]

def generate_tmpflag():
    return os.urandom(32).hex().encode()

# create mem buffer which contains dl file
chal_fd=os.memfd_create("chal")
chal_path=f'/proc/{os.getpid()}/fd/{chal_fd}'
chal_template=open("a.dl","r").read()

# compile and write dl file using given salts and your guess rules
def generate_dl(salts,guesser):
    G=f'GUESS(x) :- {guesser}.'
    S='\n'.join([f'SALT("{i.decode()}").' for i in salts])
    compiled_chal=chal_template.replace('//GUESS',G).replace("//SALTS",S)
    
    os.truncate(chal_fd,0)
    os.pwrite(chal_fd,compiled_chal.encode(),0)

# run souffle and check your answer
def run_chal(TMPFLAG):
    cmdline=f"timeout -s KILL 1s ./souffle -D- -lhash --no-preprocessor -w {chal_path}"
    proc=subprocess.Popen(args=cmdline,shell=True,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env={"TMPFLAG":TMPFLAG})
    proc.wait()
    out=proc.stdout.read()
    prefix=b'---------------\nGUESS\nans\n===============\n'
    if not out.startswith(prefix):
        raise RuntimeError(f'Souffle error? {out}')
    out=out.removeprefix(prefix)[:64]
    if out!=TMPFLAG:
        raise RuntimeError(f"Wrong guess")
    
# check user guess rules
def check_user_rules(r:str):
    if len(r) > 300:
        raise RuntimeError("rule too looong")
    e=r.encode()
    ban_chars=b'Ff.'
    for i in e:
        if i>0x7f or i<0x20 or i in ban_chars:
            raise RuntimeError("illegal char in rule")

# how many rounds will you guess
DIFFICULTY=36

def game():
    user_rules=input("your rules?\n")
    check_user_rules(user_rules)
    for i in range(DIFFICULTY):
        generate_dl(generate_salts(),user_rules)
        run_chal(generate_tmpflag())
        print(f"guess {i} is correct")
    print("Congratulations! Here is your flag:")
    os.system("/readflag")


from pow import proof
import signal

signal.alarm(25)

try:
    if os.getenv("NOPOW") is None:
        proof()
    game()
except Exception as e:
    print(e)
