The company created a VM for our ship's computer to test new software.

It looks like the company left a debug session of the VM on the network. Can you find the contents of flag.txt?

You should probably run it in Docker or at least patch our check that requires you to run it in Docker.

from pwn import *
p=remote("spaceheroes-lethal-virtualization.chals.io", 443, ssl=True, sni="spaceheroes-lethal-virtualization.chals.io")
p.interactive()

MD5SUM:

be1d30648b981fbc1ae8d60625abe667  Borson300VM.bin
