from unicorn import *
from unicorn.x86_const import *
import random
import os
import sys

shellcode = bytes.fromhex(input("Shellcode as hex string? "))
SHELLCODE_LENGTH = len(shellcode)

if SHELLCODE_LENGTH >= 25:
    print("Shellcode too long!")
    sys.exit(1)

mu = Uc(UC_ARCH_X86, UC_MODE_64)

for reg in [UC_X86_REG_RAX, UC_X86_REG_RBX, UC_X86_REG_RCX, UC_X86_REG_RDX, 
            UC_X86_REG_RSI, UC_X86_REG_RDI, UC_X86_REG_R8, UC_X86_REG_R9,
            UC_X86_REG_R10, UC_X86_REG_R11, UC_X86_REG_R12, UC_X86_REG_R13,
            UC_X86_REG_R14, UC_X86_REG_R15]:
    mu.reg_write(reg, random.randrange(1<<64))

SHELLCODE_ADDRESS = random.randrange(1<<52) * 4096
mu.mem_map(SHELLCODE_ADDRESS, 4096)
mu.mem_write(SHELLCODE_ADDRESS, os.urandom(4096))
mu.mem_write(SHELLCODE_ADDRESS, shellcode)

STACK_SIZE = 4096
STACK_TOP = random.randrange(1<<52) * 4096
mu.mem_map(STACK_TOP - STACK_SIZE, STACK_SIZE)
mu.mem_write(STACK_TOP - STACK_SIZE, os.urandom(4096))
mu.reg_write(UC_X86_REG_RSP, STACK_TOP)

def read_str(mu, addr):
    s = b''
    while True:
        c = mu.mem_read(addr, 1)
        if c == b'\0':
            return s
        s += c
        addr += 1

def read_str_array(mu, addr):
    a = []
    while True:
        s = read_str(mu, addr)
        if s == b'':
            return a
        a.append(s)
        addr += len(s)+1

def read_envp(mu, addr):
    envp = {}
    while True:
        a = int.from_bytes(mu.mem_read(addr, 8), 'little')
        if a == 0:
            return envp
        env = read_str(mu, a)
        if b'=' in env:
            k, v = env.split(b'=', 1)
            envp[k] = v
        else:
            envp[env] = b""

last_ins_len = None

def hook_mem_write(mu, access, address, size, value, user_data):
    global last_ins_len
    mu.reg_write(UC_X86_REG_RIP, address - last_ins_len)

def sys_read(mu, fd, buf, count):
    data = os.read(fd, count)
    mu.mem_write(buf, data)
    mu.reg_write(UC_X86_REG_RAX, len(data))
    hook_mem_write(mu, UC_MEM_WRITE, buf, len(data), int.from_bytes(data, 'little'), None)

def sys_write(mu, fd, buf, count):
    os.write(fd, mu.mem_read(buf, count))

def sys_open(mu, filename, flags, mode):
    fd = os.open(read_str(mu, filename), flags, mode)
    mu.reg_write(UC_X86_REG_RAX, fd)

def sys_close(mu, fd):
    os.close(fd)

def sys_execve(mu, filename, argv, envp):
    filename = read_str(mu, filename)
    argv = [filename] + read_str_array(mu, argv)
    envp = read_envp(mu, envp)
    os.execve(filename, argv, envp)

def hook_syscall64(mu, user_data):
    rax = mu.reg_read(UC_X86_REG_RAX)
    rdi = mu.reg_read(UC_X86_REG_RDI)
    rsi = mu.reg_read(UC_X86_REG_RSI)
    rdx = mu.reg_read(UC_X86_REG_RDX)

    if rax == 0:
        sys_read(mu, rdi, rsi, rdx)
    elif rax == 1:
        sys_write(mu, rdi, rsi, rdx)
    elif rax == 2:
        sys_open(mu, rdi, rsi, rdx)
    elif rax == 3:
        sys_close(mu, rdi)
    elif rax == 59:
        sys_execve(mu, rdi, rsi, rdx)
    elif rax == 60:
        sys.exit(rdi)
    else:
        print(f"Syscall {rax} not implemented!")
        sys.exit(1)

def hook_code(mu, address, size, user_data):
    global last_ins_len
    last_ins_len = size

mu.hook_add(UC_HOOK_MEM_WRITE, hook_mem_write)
mu.hook_add(UC_HOOK_CODE, hook_code)
mu.hook_add(UC_HOOK_INSN, hook_syscall64, None, 1, 0, UC_X86_INS_SYSCALL)

mu.emu_start(SHELLCODE_ADDRESS, SHELLCODE_ADDRESS+SHELLCODE_LENGTH, 0, 1337)
