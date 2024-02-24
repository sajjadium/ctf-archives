#!/usr/bin/python3
## 
## Flag-based key expansion
##
##

import hashlib
from argon2 import PasswordHasher

# Init MD5
m = hashlib.md5()

# Get flag words
flag_data = open('flag.txt','r').read()[len('brck{'):-1]
flag_words = flag_data.split('_')

# Start with strong 256 char key
init_key = "aabacadaeafa0a1a2a3a4a5a6a7a8a9bbcbdbebfb0b1b2b3b4b5b6b7b8b9ccdcecfc0c1c2c3c4c5c6c7c8c9ddedfd0d1d2d3d4d5d6d7d8d9eefe0e1e2e3e4e5e6e7e8e9ff0f1f2f3f4f5f6f7f8f90010203040506070809112131415161718192232425262728293343536373839445464748495565758596676869778798899"
print("Init key: \n\n%s\n" % init_key)

# Generate init key
m.update(init_key.encode())

# Expand key with flag words
print("Generating digests..\n")
for flag_word in flag_words:

	m.update(flag_word.encode())
	print(m.hexdigest())

# Expand the key using Argon2
ph = PasswordHasher(time_cost = 16, parallelism = 32)
h = ph.hash(m.digest())

print("\nKey after expansion: \n%s\n" % h)
