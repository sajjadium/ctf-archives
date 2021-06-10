#!/usr/local/bin/python2

from Crypto.Cipher.AES import AESCipher
import os, random, binascii
from sys import argv
import string
import sys


def padding(data):
    pad_size = 16 - (len(data) % 16)
    data = data + "".join([random.choice(string.printable) for _ in range(pad_size)])
    return data

def encrypt(data):
    return AESCipher(os.environ.get('KEY')).encrypt(padding(data))

def main():
	print "Hello! What do you want to encrypt today?"
	sys.stdout.flush()
	user_input = raw_input()
	print binascii.hexlify(encrypt(user_input + os.environ.get('FLAG')))
	sys.exit()
	
if __name__ == '__main__':
	main()