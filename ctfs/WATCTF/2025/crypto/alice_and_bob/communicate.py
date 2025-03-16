#!/usr/local/bin/python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization as ser
from cryptography.fernet import Fernet
import base64

from secret import alice_or_bob, other

def send_msg_raw(msg):
    print(f'Send to {other}:', msg.hex())

def get_msg_raw():
    line = input(f"Input response from {other}: ").strip()
    return bytes.fromhex(line)

# Exchange keys
privkey = ec.generate_private_key(ec.SECP384R1())
encoded_pubkey = privkey.public_key().public_bytes(ser.Encoding.PEM, ser.PublicFormat.SubjectPublicKeyInfo)
send_msg_raw(encoded_pubkey)
other_pubkey = ser.load_pem_public_key(get_msg_raw())
if not isinstance(other_pubkey, ec.EllipticCurvePublicKey):
    print("Hey, that's not an elliptic curve key! Connection compromised, terminating!")
shared_key = privkey.exchange(ec.ECDH(), other_pubkey)
derived_key = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=b'a salt',
    info=b'arbitrary',
).derive(shared_key)
f = Fernet(base64.urlsafe_b64encode(derived_key))

def send_msg(msg, raw=False):
    if raw:
        send_msg_raw(msg)
    else:
        send_msg_raw(f.encrypt(msg))
def recv_msg():
    return f.decrypt(get_msg_raw())

alice_or_bob(recv_msg, send_msg)
