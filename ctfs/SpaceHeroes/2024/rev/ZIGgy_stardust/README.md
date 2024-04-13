Oh, yeah Ooh Ziggy played guitar

from pwn import *
p = remote ("spaceheroes-ziggy-stardust.chals.io", 443, ssl=True, sni="spaceheroes-ziggy-stardust.chals.io")
p.interactive()
