We figured out our rocket's communication array doesn't acknowledge valid messages over a certain size. Can you help figure out what's going on?

Due to time, you should probably figure out how to solve locally first and then throw remotely.

from pwn import *
p=remote("comms.martiansonly.net",1234)
p.interactive()
