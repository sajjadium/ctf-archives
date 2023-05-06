from pwn import *

e = ELF("./four-function-heap")
libc = ELF("./libc.so.6")

p = process(e.path)

def alloc(idx, size, data="AAAA"):
  p.sendline("1")
  p.sendlineafter(":", str(idx))
  p.sendlineafter(":", str(size))
  p.sendlineafter(":", data)

  p.recvuntil(":")

def free(idx):
  p.sendline("2")
  p.sendlineafter(":", str(idx))

  p.recvuntil(":")

def show(idx):
  p.sendline("3")
  p.sendlineafter(": ", str(idx))

p.recvuntil(":")

# Your Code Here

p.interactive()
