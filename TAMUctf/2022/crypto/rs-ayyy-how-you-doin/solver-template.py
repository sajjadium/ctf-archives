from pwn import *

# This allow for some networking magic
p = remote("tamuctf.com", 443, ssl=True, sni="rs-ayyy-how-you-doin")

## YOUR CODE GOES HERE
p.interactive()
