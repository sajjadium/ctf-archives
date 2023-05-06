from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="quick-mafs")
for binary in range(5):
	instructions = p.recvline() # the server will give you instructions as to what your exploit should do
	with open("elf", "wb") as file:
		file.write(bytes.fromhex(p.recvline().rstrip().decode()))

	# send whatever data you want
	p.sendline(b"howdy".hex())
p.interactive()
