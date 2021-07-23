#!/usr/local/bin/python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii
import os

print('''
                                        ,,~~~~~~,,..
                             ...., ,'~             |
                             \    V                /
                              \  /                 /
                              ;####>     @@@@@     )
                              ##;,      @@@@@@@    )
                           .##/  ~>      @@@@@   .   .
                          ###''#>              '      '
      .:::::::.      ..###/ #>               '         '
     //////))))----~~ ## #}                '            '
   ///////))))))                          '             '
  ///////)))))))\                        '              '
 //////)))))))))))                                      '
 |////)))))))))))))____________________________________).
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||

(yeah they're not flip flops but close enough)

''')

key = os.urandom(16)
iv = os.urandom(16)
flag = open("flag.txt").read().strip()


for _ in range(3):
	print("Send me a string that when decrypted contains 'gimmeflag'.")
	print("1. Encrypt")
	print("2. Check")
	choice = input("> ")
	if choice == "1":
		cipher = AES.new(key, AES.MODE_CBC, iv)
		pt = binascii.unhexlify(input("Enter your plaintext (in hex): "))
		if b"gimmeflag" in pt:
			print("I'm not making it *that* easy for you :kekw:")
		else:
			print(binascii.hexlify(cipher.encrypt(pad(pt, 16))).decode())
	else:
		cipher = AES.new(key, AES.MODE_CBC, iv)
		ct = binascii.unhexlify(input("Enter ciphertext (in hex): "))
		assert len(ct) % 16 == 0
		if b"gimmeflag" in cipher.decrypt(ct):
			print(flag)
		else:
			print("Bad")

print("Out of operations!")
