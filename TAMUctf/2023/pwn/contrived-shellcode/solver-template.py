from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="contrived-shellcode")
p.interactive()
