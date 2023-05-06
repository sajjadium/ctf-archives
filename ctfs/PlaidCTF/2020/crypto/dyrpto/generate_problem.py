from cryptography.hazmat.backends.openssl import backend as openssl_backend
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
import json

from message_pb2 import Message

privkey = generate_private_key(3, 4096, openssl_backend)
pubkey = privkey.public_key()
pubkey_numbers = pubkey.public_numbers()
modulus = pubkey_numbers.n
publicExponent = pubkey_numbers.e
privateExponent = privkey.private_numbers().d

def get_padding():
    with open('/dev/urandom', 'rb') as f:
        return f.read(24)

def bytes_to_int(message):
    return int(message.encode('hex'), 16)

def int_to_bytes(message):
    ms = hex(message)[2:].strip('L')
    if len(ms) % 2 != 0:
        ms = '0' + ms
    return ms.decode('hex')

def pad(mi):
    return (mi << 192) | bytes_to_int(get_padding())

def unpad(mi):
    return mi >> 192

def encrypt(message):
    ciphertext = pow(pad(bytes_to_int(message)), publicExponent, modulus)
    return int_to_bytes(ciphertext)

def decrypt(ciphertext):
    plaintext = unpad(pow(bytes_to_int(ciphertext), privateExponent, modulus))
    return int_to_bytes(plaintext)

with open('message.txt', 'r') as f:
    flag_message = f.read().strip()

message = Message(id=0, msg=flag_message)
ct1 = encrypt(message.SerializeToString())
message.id = 1
ct2 = encrypt(message.SerializeToString())
print modulus
print len(message.SerializeToString())
print ct1.encode('hex')
print ct2.encode('hex')
