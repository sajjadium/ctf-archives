from pwn import *
import sys
if len(sys.argv) < 2:
    print("provide path to js source")
    raise Exception


r = remote("babygc.chal.perfect.blue", 1337)

f = open(sys.argv[1],"r")
src = f.read()
f.close()

r.sendlineafter("Your js file size:",str(len(src)))
r.sendlineafter(":",src)
r.interactive()
