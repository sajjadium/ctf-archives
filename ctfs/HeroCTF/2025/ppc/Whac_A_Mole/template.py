from pwn import *

# Adjust depending challenge adress
HOST = "localhost"
PORT = 8001

io = remote(HOST, PORT)

while True:
    line = io.recvline()
    if b"IMAGE:" in line:
        # Read the base64 encoded image
        b64img = io.recvline().strip()
        log.info(f"Got image (length {len(b64img)})")

        # The server asks for answer
        io.recvuntil(b">> ")

        # TODO: process image and compute answer
        answer = 0

        # Send back the answer
        io.sendline(str(answer).encode())

    elif b"Wrong answer!" in line or b"Hero" in line:
        # Print the line and exit if it's an error or contains the flag
        print(line.decode().strip())
        io.close()
        break
    else:
        log.info(line.decode().strip())