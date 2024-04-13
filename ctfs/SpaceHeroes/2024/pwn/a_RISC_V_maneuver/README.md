sorry... we could not afford tom hanks

from pwn import *
io = remote ("spaceheroes-a-riscv-maneuver.chals.io", 443, ssl=True, sni="spaceheroes-a-riscv-maneuver.chals.io")
io.interactive()
