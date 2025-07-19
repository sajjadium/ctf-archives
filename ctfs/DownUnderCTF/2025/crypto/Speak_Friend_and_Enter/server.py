#!/usr/bin/env python3

from Crypto.Hash import CMAC, SHA512
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Util.number import long_to_bytes, bytes_to_long
from binascii import unhexlify
import random, json, string

from cryptosecrets import NIST_SP_800_38B_Appendix_D1_K, flag

## Generated once and MAC saved
# r = RSA.generate(2048)
# cc = CMAC.new(NIST_SP_800_38B_Appendix_D1_K, ciphermod=AES)
# server_cmac_publickey = cc.update(long_to_bytes(r.n)).digest()

server_cmac_publickey = unhexlify('9d4dfd27cb483aa0cf623e43ff3d3432')

challenge_string = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(48)]).encode()

print(f"Here is your challenge string: {challenge_string.decode()}")
print('Enter your signature for verification as a json string {"public_key": (int), "signature" : (int)}:') 
js = input()

try:
    j = json.loads(js)
    public_key = j['public_key']
    signature = j['signature']
except Exception as e:
    print(f"Error in input: {e}")
    exit(0)


## Check public key hash matches server
cc = CMAC.new(NIST_SP_800_38B_Appendix_D1_K, ciphermod=AES)
mac = cc.update(long_to_bytes(public_key)).digest()

if mac != server_cmac_publickey:
    print("Public key MAC did not match")
    exit(0)

if public_key.bit_length() != 2048:
    print("Public key size incorrect")
    exit(0)

r = RSA.construct((public_key, 65537))
s = bytes_to_long(SHA512.new(challenge_string).digest())

if pow(signature, 65537, r.n) == s:
    print(f'Signature verified! Here is your flag: {flag}')
    exit(0)
else:
    print("Signature incorrect")
    exit(0)
