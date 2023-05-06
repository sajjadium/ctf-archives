from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="lucky")
p.interactive()
