#!/usr/bin/env python3

from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Protocol.KDF import HKDF
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.number import long_to_bytes
import os

cwd = os.path.dirname(__file__)
ca_pubkey = ECC.import_key(open(os.path.join(cwd, 'public/ca-pubkey.pem'), 'r').read())
server_privkey = ECC.import_key(open(os.path.join(cwd, 'private/server-privkey.pem'), 'r').read())

print('Hello client!')
print(server_privkey.public_key().export_key(format='PEM'))

print('Please provide your certificate:')
try:
    subject_line = input()
    assert subject_line.startswith('SUBJECT=')
    subject = subject_line[8:]
    client_pubkey_pem = '\n'.join(input() for _ in range(4))
    client_pubkey = ECC.import_key(client_pubkey_pem)
    signature_hex = input()
    tbs = f'{subject_line}\n{client_pubkey_pem}'
    verifier = DSS.new(ca_pubkey, 'fips-186-3')
    verifier.verify(SHA256.new(tbs.encode()), bytes.fromhex(signature_hex))
except:
    print('Bad certificate')
    exit(-1)

shared_secret = (server_privkey.d * client_pubkey.pointQ).x
shared_secret = long_to_bytes(shared_secret)

client_nonce = bytes.fromhex(input('Client nonce: '))
if not client_nonce:
    print('Invalid client nonce')
    exit(-1)

server_nonce = os.urandom(16)
print('Server nonce:', server_nonce.hex())

shared_nonce = SHA256.new(client_nonce + shared_secret + server_nonce).digest()
print('Shared nonce:', shared_nonce.hex())

derived_key = HKDF(shared_secret + client_nonce + server_nonce + shared_nonce,
                   32,
                   salt=b'DUCTF-2023',
                   hashmod=SHA256)

aes = AES.new(derived_key, AES.MODE_ECB)
msg = f'Hello {subject}, it\'s nice to meet you.'
if subject == 'admin':
    flag = open(os.path.join(cwd, 'flag.txt'), 'r').read()
    msg += f' Here is your flag: {flag}'
print(aes.encrypt(pad(msg.encode(), 16)).hex())
