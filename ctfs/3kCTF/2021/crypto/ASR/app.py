import binascii
import hashlib
import random
import os
import string

import OpenSSL.crypto as crypto

rsa_p_not_prime_pem = """\n-----BEGIN RSA PRIVATE KEY-----\nMBsCAQACAS0CAQcCAQACAQ8CAQMCAQACAQACAQA=\n-----END RSA PRIVATE KEY-----\n"""
invalid_key = crypto.load_privatekey(crypto.FILETYPE_PEM, rsa_p_not_prime_pem)
error_msg = "Pycrypto needs to be patched!"

try:
    invalid_key.check()
    raise RuntimeError(error_msg)
except crypto.Error:
    pass

# proof of work to prevent any kind of bruteforce :-)
prefix = "".join(random.choice(string.ascii_lowercase) for _ in range(6))
print("Find a string s such that sha256(prefix + s) has 24 binary leading zeros. Prefix = '{}'".format(prefix))
pow_answer = input("Answer: ")

assert hashlib.sha256((prefix + pow_answer).encode()).digest()[:3] == b"\x00\x00\x00"

# v v v challenge starts here v v v
print("\n\nHello, i hope you can help me out. I might reward you something in return :D")

key = ""
# read in key
while True:
    buffer = input()
    if buffer:
        key += buffer + "\n"
    else:
        break


key = crypto.load_privatekey(crypto.FILETYPE_PEM, key)
private_numbers = key.to_cryptography_key().private_numbers()
assert key.check()

d = private_numbers.d
p = private_numbers.p
q = private_numbers.q
N = p * q

# i dont like small numbers
assert d > 1337 * 1337 * 1337 * 1337 * 1337

# and i dont like even numbers
assert N % 2 != 0

if pow(820325443930302277, d, N) == 4697802211516556112265788623731306453433385478626600383507434404846355593172244102208887127168181632320398894844742461440572092476461783702169367563712341297753907259551040916637774047676943465204638648293879569:
    with open("flag") as fd:
        print(fd.read())
else:
    print("Nop. :(")
