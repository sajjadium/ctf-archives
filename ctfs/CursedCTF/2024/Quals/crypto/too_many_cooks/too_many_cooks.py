BANNER = """\
I was alarmed to learn that cryptographers have broken 31 out of 64 rounds of SHA256.
To defend against cryptographers, I made my own hash function.
I hear rolling your own crypto is bad, so I merely composed existing hash functions.
~ retr0id

"""

import asyncio
import hashlib
from fastcrc.crc64 import ecma_182 as crc64 # https://pypi.org/project/fastcrc/
import xxhash # https://pypi.org/project/xxhash/

def megahash(msg: bytes) -> bytes:
	h0 = hashlib.blake2s(msg).digest() # avoid NIST backdoors
	h1 = xxhash.xxh64_digest(h0)       # gotta go fast
	h1 += crc64(msg).to_bytes(8)       # but 64 bits isn't enough security, lets add some more
	h2 = hashlib.sha3_256(h1).digest() # and we still want a NIST-approved output!
	return h2


try:
	from flag import FLAG
except ImportError:
	print("[!] using placeholder flag")
	FLAG = "flag{placeholder}"

HOST = "0.0.0.0"
PORT = 4200
TIMEOUT = 60

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
	writer.write(BANNER.encode())
	writer.write(b"Show me a hash collision for sha3_256( xxh64(blake2s_256(msg)) || crc64(msg) )\n\n")

	writer.write(b"msg1 (hex): ")
	await writer.drain()
	line = await reader.readline()
	try:
		msg1 = bytes.fromhex(line.decode())
	except:
		writer.write(b"invalid input\n")
		await writer.drain()
		return
	
	writer.write(b"msg2 (hex): ")
	await writer.drain()
	line = await reader.readline()
	try:
		msg2 = bytes.fromhex(line.decode())
	except:
		writer.write(b"invalid input\n")
		await writer.drain()
		return
	
	if len(msg1) > 1024 or len(msg2) > 1024:
		writer.write(b"too big!\n")
		await writer.drain()
		return

	if msg1 == msg2:
		writer.write(b"You can't fool me that easily!\n")
		await writer.drain()
		return

	h1 = megahash(msg1)
	h2 = megahash(msg2)

	writer.write(f"\nh1 = {h1.hex()}\n".encode())
	writer.write(f"h2 = {h2.hex()}\n".encode())

	if h1 == h2:
		writer.write(f"\nCongrats!\n{FLAG}\n".encode())
	else:
		writer.write(b"\n:(\n")
	
	await writer.drain()

async def handle_client_safely(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
	peer = writer.get_extra_info("peername")
	print("[+] New connection from", peer)
	try:
		await asyncio.wait_for(handle_client(reader, writer), TIMEOUT)
		writer.close()
		print("[+] Gracefully closed connection from", peer)
	except ConnectionResetError:
		print("[*] Connection reset by", peer)
	except asyncio.exceptions.TimeoutError:
		print("[*] Connection timed out", peer)
		writer.close()

async def main():
	server = await asyncio.start_server(handle_client_safely, HOST, PORT)
	print("[+] Server started")
	async with server:
		await server.serve_forever()

if __name__ == "__main__":
	asyncio.run(main())
