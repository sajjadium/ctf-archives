#!/usr/local/bin/python
import ctypes
from unicorn import *
from unicorn.x86_const import *

libc = ctypes.CDLL(None)
LOAD_ADDR, CODE_SIZE   = 0x555555554000, 0x10000
STACK_ADDR, STACK_SIZE = 0x7ffffffdd000, 0x22000

def emu_syscall(mu, _user_data):
    ret = libc.syscall(
        mu.reg_read(UC_X86_REG_RAX),
        mu.reg_read(UC_X86_REG_RDI), mu.reg_read(UC_X86_REG_RSI),
        mu.reg_read(UC_X86_REG_RDX), mu.reg_read(UC_X86_REG_R10),
        mu.reg_read(UC_X86_REG_R8) , mu.reg_read(UC_X86_REG_R9),
    )
    mu.reg_write(UC_X86_REG_RAX, ret)

def chk_syscall(mu, addr, size, _user_data):
    insn = mu.mem_read(addr, size)
    if insn == bytearray(b'\x0f\x05'): # syscall
        sys_num = mu.reg_read(UC_X86_REG_RAX)
        if sys_num != 60:
            print(f"[-] System call not allowed: {sys_num}")
            mu.emu_stop()

def emulate(code):
    assert len(code) <= CODE_SIZE, "Too long shellcode"
    mu = Uc(UC_ARCH_X86, UC_MODE_64)
    # Map code memory
    mu.mem_map(LOAD_ADDR, CODE_SIZE, UC_PROT_READ | UC_PROT_EXEC)
    mu.mem_write(LOAD_ADDR, code)
    # Map stack memory
    mu.mem_map(STACK_ADDR, STACK_SIZE, UC_PROT_READ | UC_PROT_WRITE)
    mu.reg_write(UC_X86_REG_RSP, STACK_ADDR + STACK_SIZE)
    # Set hook
    mu.hook_add(UC_HOOK_CODE, chk_syscall)
    mu.hook_add(UC_HOOK_INSN, emu_syscall, None, 1, 0, UC_X86_INS_SYSCALL)
    # Start emulation
    try:
        mu.emu_start(LOAD_ADDR, LOAD_ADDR + len(code), UC_SECOND_SCALE*3)
    except UcError:
        print("[-] Segmentation fault")

if __name__ == '__main__':
    emulate(bytes.fromhex(input("shellcode: ")))
