import os
import secrets

flag = "REDACATED"
xor_key = secrets.token_bytes(8)

def xor(message, key):
    return bytes([message[i] ^ key[i % len(key)] for i in range(len(message))])

encrypted_flag = xor(flag.encode(), xor_key).hex()

with open("flag.enc", "w") as f:
    f.write("Flag: "+encrypted_flag)