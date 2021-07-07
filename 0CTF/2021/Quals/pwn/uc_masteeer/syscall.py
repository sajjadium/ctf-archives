#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from unicorn import *
from unicorn.x86_const import *
import os.path
import sys


def hook_syscall(uc, user_data):
    arg_regs = [UC_X86_REG_RDI, UC_X86_REG_RSI, UC_X86_REG_RDX, UC_X86_REG_R10, UC_X86_REG_R8, UC_X86_REG_R9]
    rax = uc.reg_read(UC_X86_REG_RAX)
    if rax in SYSCALL_MAP.keys():
        ff, n = SYSCALL_MAP[rax]
        args = []
        while n > 0:
            args.append(uc.reg_read(arg_regs.pop(0)))
            n -= 1
        try:
            ret = ff(uc, *args) & 0xffffffffffffffff
        except Exception as e:
            uc.emu_stop()
            return
    else:
        ret = 0xffffffffffffffff
    uc.reg_write(UC_X86_REG_RAX, ret)


def sys_read(uc, fd, buf_addr, size):
    if fd != 0:
        return -1
    data = ''
    data = os.read(0, size)
    assert len(data) <= size < 0x100
    uc.safe_mem_write(buf_addr, data)
    return len(data)


def sys_write(uc, fd, buf_addr, size):
    if fd != 1:
        return -1
    data = uc.mem_read(buf_addr, size)
    assert len(data) <= size < 0x100
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    return len(data)


def sys_exit(uc, error_code):
    uc.emu_stop()
    return error_code


SYSCALL_MAP = {
    0: (sys_read, 3),
    1: (sys_write, 3),
    60: (sys_exit, 1),
}

