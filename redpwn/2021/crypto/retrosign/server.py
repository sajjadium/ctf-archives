#!/usr/local/bin/python

from Crypto.Util.number import getPrime, bytes_to_long
from Crypto.Hash import SHA256
from binascii import unhexlify
from secrets import randbelow

with open('flag.txt','r') as f:
    flag = f.read().strip()

def sha256(val):
    h = SHA256.new()
    h.update(val)
    return h.digest()

def execute(cmd):
    if cmd == "sice_deets":
        print(flag)
    elif cmd == "bad_signature":
        print("INTRUSION DETECTED!")
    else:
        print("Command unknown.")

def authorize_command(cmd, sig):
    assert len(sig) == 128*2
    a = bytes_to_long(sig[:128])
    b = bytes_to_long(sig[128:])
    if (a**2 + k*b**2) % n == bytes_to_long(sha256(cmd)):
        execute(cmd.decode())
    else:
        execute("bad_signature")

p = getPrime(512)
q = getPrime(512)
n = p * q
k = randbelow(n)
def interact():
    print("===============================================================================")
    print("This mainframe is protected with state-of-the-art intrusion detection software.")
    print("All commands are passed through a signature-based filter.")
    print("===============================================================================")
    print("The following configuration is in place:")
    print(f"n = {n};\nk = {k};")
    print("Server configured.")
    cmd = input(">>> ").strip().lower().encode()
    sig = unhexlify(input("$$$ "))
    authorize_command(cmd, sig)
    print("Connection closed.")

if __name__ == "__main__":
    try:
        interact()
    except:
        print("An error has occurred.")
