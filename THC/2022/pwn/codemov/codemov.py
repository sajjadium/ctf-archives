#!/usr/bin/env python3

from pwn import *

context.arch = 'amd64'

print("Enter your shellcode (80 bytes max): ")

shellcode = []

while True:
    try:
        code = input().replace(';', '').lower().strip()
        if code == "end":
            break
        if not code.startswith("mov"):
            log.failure("Invalid instruction")
            exit()
        shellcode.append(code)
    except EOFError:
        break

shellcode = asm('\n'.join(shellcode))

log.info('Executing shellcode')

r = process('./executor', alarm=30)
r.sendline(shellcode)
r.wait_for_close()

log.success('kthxbye')