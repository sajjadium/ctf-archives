from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="labyrinth")
for binary in range(5):
  with open("elf", "wb") as file:
    file.write(bytes.fromhex(p.recvline().rstrip().decode()))

  # send whatever data you want
  p.sendline(b"howdy".hex())
p.interactive()
