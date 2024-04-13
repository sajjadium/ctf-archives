from pwn import *
io = remote ("spaceheroes-checkpoint.chals.io", 443, ssl=True, sni="spaceheroes-checkpoint.chals.io")
io.interactive()
