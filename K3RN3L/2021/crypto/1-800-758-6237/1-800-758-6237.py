#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Cipher import AES
import os, time, random

# Local imports
with open('flag.txt', 'rb') as f:
	FLAG = f.read()
	f.close()


def leak(drip):
	rinds = sorted(random.sample(range(len(drip)+1), 16))

	for i in range(len(rinds)):
		ind  = rinds[i] + i*len(b'*drip*')
		drip = drip[:ind] + b'*drip*' + drip[ind:]

	aes = AES.new(key=server_key, mode=AES.MODE_CTR, nonce=b'NEEDaPLUMBER')
	return aes.encrypt(drip).hex()


server_key = os.urandom(16)

while True:

	print(leak(FLAG))

	time.sleep(1)