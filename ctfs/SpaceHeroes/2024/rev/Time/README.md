Tick tock tick tock tick tock...

from pwn import *
p=remote("spaceheroes-time.chals.io", 443, ssl=True, sni="spaceheroes-time.chals.io")
p.interactive()

md5(Time) = fb5d6082ec4555aa97716760c80d49e9
