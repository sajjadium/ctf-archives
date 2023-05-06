#!/usr/bin/env python3

import asyncio
from Cryptodome.Cipher import AES  # pip3 install pycryptodomex
import os

from REDACTED import FLAG
assert(type(FLAG) is str)
assert(len(FLAG) == 32)

HOST = "0.0.0.0"
PORT = 1209

NUM_SLOTS = 8
SLOT_SIZE = 16
MAX_CMDS = 1000
TIMEOUT = 60

HELPMSG = f"""
Welcome to Santa's Super-Secure Secret Storage Service

There are {NUM_SLOTS} write-only keyslots.
There are {NUM_SLOTS} read/write dataslots.

You can encrypt the data in a chosen dataslot,
with a key from a chosen keyslot.

Once a keyslot is written, it cannot be read back.
This allows the elves to securely process encrypted data,
without being able to access the keys.

For example, to encrypt the string "topsecretmessage"
with key deadbeefdeadbeefdeadbeefdeadbeef:

write_key 3 deadbeefdeadbeefdeadbeefdeadbeef hex
write_data 7 topsecretmessage ascii
encrypt 3 2 7
read_data 2


AVAILABLE COMMANDS:

"""

class SecurityEngine():
	def __init__(self):
		self.commands = {
			"help":       (self.cmd_help,       []),
			"encrypt":    (self.cmd_encrypt,    ["keyslot", "dest", "src"]),
			"read_data":  (self.cmd_read_data,  ["dataslot"]),
			"write_data": (self.cmd_write_data, ["dataslot", "data", "encoding"]),
			"write_key":  (self.cmd_write_key,  ["keyslot", "data", "encoding"]),
			"exit":       (self.cmd_exit,       [])
		}
		self.running = True
		self.counter = 0
		self.keyslots  = bytearray(SLOT_SIZE * NUM_SLOTS)
		self.dataslots = bytearray(SLOT_SIZE * NUM_SLOTS)

	def _parse_slot_idx(self, i):
		i = int(i)
		if i < 0 or i >= NUM_SLOTS:
			raise Exception("Slot index out of range")
		return i
	
	def _parse_data_string(self, data, encoding):
		if encoding == "hex":
			if len(data) != SLOT_SIZE * 2:
				raise Exception("Invalid data length")
			return bytes.fromhex(data)
		elif encoding == "ascii":
			if len(data) != SLOT_SIZE:
				raise Exception("Invalid data length")
			return data.encode()
		raise Exception("Invalid encoding")

	def run_cmd(self, cmd):
		self.counter += 1
		if self.counter > MAX_CMDS:
			self.running = False
			return "ERROR: MAX_CMDS exceeded"

		cmd = cmd.strip()
		if not cmd: return ""

		op, *args = cmd.split()

		if op not in self.commands:
			return "ERROR: command not found"
		
		cmdfn, cmdargs = self.commands[op]

		if len(args) != len(cmdargs):
			return "ERROR: wrong number of arguments"

		return cmdfn(*args)

	def cmd_help(self):
		"""print this message"""

		result = HELPMSG
		for cmdname, (cmdfn, cmdargs) in self.commands.items():
			result += f"{cmdname + ' ' + ' '.join(cmdargs): <34} {cmdfn.__doc__}\n"

		return result

	def cmd_encrypt(self, keyslot, dest, src):
		"""encrypt src dataslot with chosen keyslot, write the result to dest dataslot"""

		try: keyslot = self._parse_slot_idx(keyslot)
		except: return "ERROR: Invalid keyslot index"

		try: dest = self._parse_slot_idx(dest)
		except: return "ERROR: Invalid dest index"
		
		try: src = self._parse_slot_idx(src)
		except: return "ERROR: Invalid src index"

		plaintext = self.dataslots[SLOT_SIZE*src:SLOT_SIZE*(src+1)]
		key = self.keyslots[SLOT_SIZE*keyslot:SLOT_SIZE*(keyslot+1)]
		ciphertext = AES.new(key=key, mode=AES.MODE_ECB).encrypt(plaintext)
		self.dataslots[SLOT_SIZE*dest:SLOT_SIZE*(dest+1)] = ciphertext

		return f"dataslot[{dest}] <= AES(key=keyslot[{keyslot}], data=dataslot[{src}])"
	
	def cmd_read_data(self, slot_idx):
		"""read a chosen dataslot"""

		try: slot_idx = self._parse_slot_idx(slot_idx)
		except: return "ERROR: Invalid index"

		return self.dataslots[SLOT_SIZE*slot_idx:SLOT_SIZE*(slot_idx+1)].hex()

	def cmd_write_data(self, slot_idx, data, encoding):
		"""write data to a chosen dataslot"""

		try: slot_idx = self._parse_slot_idx(slot_idx)
		except: return "ERROR: Invalid index"

		try: data = self._parse_data_string(data, encoding)
		except: return "ERROR: Invalid data length or encoding"

		self.dataslots[SLOT_SIZE*slot_idx:SLOT_SIZE*slot_idx+len(data)] = data
		
		return f"dataslot[{slot_idx}] <= {data.hex()}"

	def cmd_write_key(self, slot_idx, data, encoding):
		"""write data to a chosen keyslot"""

		try: slot_idx = self._parse_slot_idx(slot_idx)
		except: return "ERROR: Invalid index"

		try: data = self._parse_data_string(data, encoding)
		except: return "ERROR: Invalid data length or encoding"

		self.keyslots[SLOT_SIZE*slot_idx:SLOT_SIZE*slot_idx+len(data)] = data

		return f"keyslot[{slot_idx}] <= {data.hex()}"

	def cmd_exit(self):
		"""exit the session"""

		self.running = False
		return "bye"

async def handle_client(reader, writer):
	se = SecurityEngine()

	# provision keyslot 5 with a secure random key, and use it to encrypt the flag
	# since keyslots are write-only, the flag cannot be recovered!
	se.run_cmd(f"write_key 5 {os.urandom(SLOT_SIZE).hex()} hex")
	se.run_cmd(f"write_data 0 {FLAG[:16]} ascii")
	se.run_cmd(f"write_data 1 {FLAG[16:]} ascii")
	se.run_cmd(f"encrypt 5 0 0")
	se.run_cmd(f"encrypt 5 1 1")

	while se.running:
		command = await reader.readline()

		try: command = command.decode()
		except: continue

		result = se.run_cmd(command)
		writer.write(result.encode() + b"\n")
		await writer.drain()

async def handle_client_safely(reader, writer):
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

asyncio.run(main())
