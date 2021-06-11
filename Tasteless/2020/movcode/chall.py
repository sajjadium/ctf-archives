#!/usr/bin/env python3
import re
import sys
import subprocess

from time import sleep
from shutil import rmtree
from tempfile import TemporaryDirectory


COMPILE_CMD = ['gcc', '-c', 'movcode.s']
LINK_CMD = ['ld', '-melf_x86_64', '-z', 'noexecstack', 'movcode.o']
RUN_CMD = ['setarch', 'x86_64', '-R', './a.out']

TEMPLATE = '''
.intel_syntax noprefix

.text
.globl  _start

_start:
    xor rcx, rcx
    mov rdx, 0x1000
    mov rsp, 0x7ffffffff000
u_no_env:
    push rax
    dec rdx
    cmp rdx, 0x00
    jnz u_no_env
    mov rsp, 0x7ffffffff000

    {}
    mov rax, 1
    syscall

    mov rdi, 0x42
    mov rax, 0x3c
    syscall
'''

class TastelessException(Exception):
    pass

def print(string):
    for c in string:
        sys.stdout.write(c)
        sys.stdout.flush()
        sleep(.1)
    sys.stdout.write("\n")

def create_assembly_file(dir):

    filter = re.compile(r'^mov\s[\w\[\],\s]*;?$')

    print("SHOW ME WHAT YOU GOT: \n")
    movcode = []
    for line in sys.stdin:
        if (line == '\n'):
            break
        movcode += [line]


    for l in movcode:
        if filter.match(l) is None:
            raise TastelessException("THIS AINT NO MOVCODE!!!")


    with open('{}/movcode.s'.format(dir.name), 'w') as f:
        f.write( TEMPLATE.format( ''.join(movcode)) )


def compile_and_link(dir):

    if subprocess.run(COMPILE_CMD, cwd=dir.name).returncode:
        raise TastelessException("NO COMPILE.")
    if subprocess.run(LINK_CMD, cwd=dir.name).returncode:
        raise TastelessException("NO LINK.")


def check_output(dir, output):
    movret = subprocess.run(RUN_CMD, cwd=dir.name, stdout=subprocess.PIPE,
                            timeout=1, env={})

    if movret.returncode != 0x42:
        raise TastelessException("Hmmm.... NOPE!")

    if movret.stdout != output:
        raise TastelessException("NOPE!")


def give_flag():
    print("GG. WE GIVE U FLAG: ")
    with open('flag.txt', 'r') as f:
        flag = f.read()
    print(flag)

def main():

    dir = TemporaryDirectory()
    try:
        create_assembly_file(dir)
        compile_and_link(dir)

        print("RUN ONCE ...")
        check_output(dir, b'TASTE')
        print("GOT RIGHT RESPONSE!\n")

        print("RUN TWICE ...")
        check_output(dir, b'LESS!')
        print("THAT WAS NICE!\n")

        give_flag()

    except TastelessException as e:
        print(e.args[0])
    except Exception as e:
        print("WHAT AR U DOING?!?")




if __name__ == '__main__':
    main()
