#!/usr/bin/env python
from unicorn import *
from unicorn.x86_const import *
import os
import sys
import struct
import hashlib

FLAG = 'flag{xxxx}'
CODE = 0xdeadbeef000
DATA = 0xbabecafe000
finished = False
insn_count = 0
block_count = 0


def hook_block(uc, address, size, user_data):
    global block_count
    block_count += 1
    if block_count > 1:
        print('No cheating!')
        uc.emu_stop()


def hook_code(uc, address, size, user_data):
    global insn_count, finished
    insn_count += 1
    if address == CODE + 0x2000:
        finished = True


def play():
    global finished
    uc = Uc(UC_ARCH_X86, UC_MODE_64)

    code = os.read(0, 0x2000)

    uc.mem_map(CODE, 0x3000, UC_PROT_READ | UC_PROT_EXEC)
    uc.mem_write(CODE, code)
    uc.mem_write(CODE + 0x2000, b'\xf4')

    check_data = os.urandom(50)
    uc.mem_map(DATA, 0x1000, UC_PROT_READ | UC_PROT_WRITE)
    uc.mem_write(DATA, check_data)

    uc.hook_add(UC_HOOK_CODE, hook_code)
    uc.hook_add(UC_HOOK_BLOCK, hook_block)

    try:
        uc.emu_start(CODE, CODE + 0x3000)
    except UcError as e:
        finished = False
        return False

    user_data = uc.mem_read(DATA + 0x800, 16)
    if user_data == hashlib.md5(check_data).digest():
        print('Nice.')
        return True
    else:
        print('0ops.')
        return False


if __name__ == '__main__':
    print('Welcome to uc_baaaby')
    win = play()
    if finished and win:
        print("Congratulation! You've reached the end!")
        print(f'You took {insn_count} seconds.\n')
        if insn_count < 0x233:
            print('How is this possible??? Even Bolt can\'t run this fast.')
            print('Prize for you:', FLAG)
        elif insn_count < 0x300:
            print('Come on. You can be faster.')
        else:
            print('Gege jia you.')

