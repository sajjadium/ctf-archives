#!/usr/bin/python3
import random

class randomGenerator:
	def __init__(self):
		self.buffer = 0;
		self.bitsLeft = 0;

	def getRand(self,bits):
		while self.bitsLeft < bits :
			self.buffer = self.buffer + (random.getrandbits(1024) << self.bitsLeft);
			self.bitsLeft += 1024;
		uwu = self.buffer & ((1 << bits) - 1);
		self.buffer = self.buffer >> bits;
		self.bitsLeft -= bits;
		return uwu;

# A secret message
# I heard a rumor that the message has a SUPER long string of ORZORZORZORZORZORZ.... of reasonably long length
msg = open('message.txt','rb').read().hex();
last_ct = 0;
outputMessage = "";
generator = randomGenerator();

for i in range(len(msg) // 2):
	block_pt = int(msg[i * 2:i * 2 + 2],16);
	block_ct = block_pt ^ last_ct;
	last_ct = block_ct;
	block_uwu = block_ct ^ generator.getRand(8);
	outputMessage += hex(block_uwu)[2:].zfill(2);

print(outputMessage);
