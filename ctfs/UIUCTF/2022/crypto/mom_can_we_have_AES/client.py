from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

import random
import string

from fields import cert, block_size
from secret import flag

cipher_suite = {"AES.MODE_CBC": AES.MODE_CBC, "AES.MODE_CTR": AES.MODE_CTR, "AES.MODE_OFB": AES.MODE_OFB, "AES.MODE_EAX": AES.MODE_EAX, "AES.MODE_ECB": AES.MODE_ECB}

########## Client Hello ##########
# Cipher suite
print(*cipher_suite.keys(), sep=', ')

client_random = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(4))
# Client random
print(client_random)

########## Server Hello ##########

# verify server
# Enter signed certificate
server_signature_hex = input()
server_signature = bytearray.fromhex(server_signature_hex)
public_key = RSA.import_key(open("receiver.pem").read())
cipher_hash = SHA256.new(cert)
verifier = PKCS1_v1_5.new(public_key)

if not verifier.verify(cipher_hash, server_signature):
    print("Mom told me not to talk to strangers.")
    exit()

# Enter selected cipher suite
input_encryptions_suite = input()
if len(input_encryptions_suite) == 0:
    print(" nO SeCUriTY :/")
    exit()

selected_cipher_suite = {}
input_encryptions_suite = input_encryptions_suite.split(", ")
for method in input_encryptions_suite:
    if method in cipher_suite:
        selected_cipher_suite[method] = cipher_suite[method]

if len(selected_cipher_suite) == 0:
    print("I'm a rebellious kid who refuses to talk to people who don't speak my language.")
    exit()

# Enter server random
server_random = input()

########## Client Cipherspec finished & Client KeyExchange ##########
premaster_secret = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

cipher_rsa = PKCS1_OAEP.new(public_key)
premaster_secret_encrypted = cipher_rsa.encrypt(premaster_secret.encode()).hex()
# Encrypted premaster secret
print(premaster_secret_encrypted)

session_key = SHA256.new((client_random + server_random + premaster_secret).encode()).hexdigest()

chosen_cipher_name = next(iter(selected_cipher_suite))
# Using encryption mode
print(chosen_cipher_name)
cipher = AES.new(session_key.encode()[:16], cipher_suite[chosen_cipher_name])

# Encrypted finish message
print(cipher.encrypt(pad(b"finish", block_size)).hex())

########## ServerKeyExchange & CipherSpec Finished ##########
# Confirm finish
finish_msg = input()
assert(finish_msg == "finish")

########## Communication ##########

while True:
    prefix = input()
    if len(prefix) != 0:
        prefix = bytearray.fromhex(prefix)
        extended_flag = prefix + flag
    else:
        extended_flag = flag
    
    ciphertext = cipher.encrypt(pad(extended_flag, block_size)).hex()
    print(str(ciphertext))
