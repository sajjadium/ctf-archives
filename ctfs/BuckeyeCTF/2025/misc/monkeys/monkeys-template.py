from pwn import *

io = remote("monkeys.challs.pwnoh.io", 1337, ssl=True)

io.recvuntil(b"code:\n")
io.sendline(b"""
function(input)
    return input .. string.char(0x98)
end
""")
io.sendline(b"EOF")

data = io.recvline() + io.recvline()
if b"Output bytestring: " in data:
    output = bytes.fromhex(data.split(b": ")[1].strip().decode())
    info(f"{len(output)=}")

    # transform output back into input...
    input = output

    io.sendline(input.hex().encode())
    print(io.recvall().decode().strip())
else:
    print((data + io.recvall()).decode().strip())
