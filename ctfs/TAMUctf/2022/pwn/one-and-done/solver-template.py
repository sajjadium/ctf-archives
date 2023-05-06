from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="one-and-done")
p.interactive()
