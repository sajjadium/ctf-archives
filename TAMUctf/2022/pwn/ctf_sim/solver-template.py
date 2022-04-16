from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="ctf-sim")
p.interactive()
