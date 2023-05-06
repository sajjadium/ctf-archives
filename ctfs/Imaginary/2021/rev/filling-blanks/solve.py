from pwn import *
from ctypes import CDLL, c_int

exe = ELF('./predict', checksec=False)
libc = CDLL('libc.so.6')

p = process(exe.path)
# p = remote('20.94.210.205', 1337)

constants = [____.rand() for i in range(4)]

p.recvuntil('flag: \n')

seed = libc.____(0) // 10
libc.srand(seed)

for i in range(4):
	random = libc.rand()
	constants[i] = _____(constants[i] * (random % 1000))

constants = [i._____ for i in constants]

guess = c_int(sum(constants)).value

p.sendline(str(guess))
print(p.recv())