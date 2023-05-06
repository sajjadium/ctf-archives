from pwn import *

pc = process("./chall")
# pc = remote("",)
shell_code = b""  # PUT YOUR SHELL CODE HERE
pc.sendline(shell_code)
pc.interactive()
