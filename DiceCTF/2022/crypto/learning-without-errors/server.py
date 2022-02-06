#!/usr/local/bin/python3

import json

from challenge import Challenge

poly_degree = 1024
ciph_modulus = 1 << 100

print('Please hold, generating keys...', flush=True)
chal = Challenge(poly_degree, ciph_modulus)
print('Welcome to the Encryption-As-A-Service Provider of the Future, powered by the latest in Fully-Homomorphic Encryption!')

data = input('Provide your complex vector as json to be encrypted: ')
data = json.loads(data)

ciph = chal.encrypt_json(data)
string_ciph = json.dumps(chal.dump_ciphertext(ciph))
print('Encryption successful, here is your ciphertext:', string_ciph)

plain = chal.decrypt_ciphertext(ciph)
string_plain = json.dumps(chal.dump_plaintext(plain))
print('To verify that the encryption worked, here is the corresponding decryption:', string_plain)

e_flag = chal.encrypt_flag()
string_flag = json.dumps(chal.dump_ciphertext(e_flag))
print('All done, here\'s an encrypted flag as a reward:', string_flag)

print('Enjoy DiceCTF!')
