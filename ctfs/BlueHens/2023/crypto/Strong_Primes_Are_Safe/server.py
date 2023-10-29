import random
from Crypto.Util import number, Padding
from Crypto.Cipher import AES
import flag
import logging
import hashlib
import json


GENERATOR = 2
KEY_BYTES = 16
PRIME_BITS = 2048



logging.basicConfig(filename="auth.log",level=logging.INFO,format="%(message)s")

def authenticate(primes):
    RAND = random.SystemRandom()
    p: int = RAND.choice(primes)
    b = RAND.randint(2,p-2)
    print(hex(p)[2:])
    A = int(input(),16)
    B = pow(GENERATOR,b,p)
    print(hex(B)[2:])
    ss = hashlib.sha256(pow(A,b,p).to_bytes(PRIME_BITS//8,'big')).digest()[:KEY_BYTES]
    iv = RAND.getrandbits(AES.block_size*8)
    iv = iv.to_bytes(AES.block_size,'big')
    cipher = AES.new(ss,AES.MODE_CBC,iv=iv)
    ct = cipher.encrypt(Padding.pad(flag.FLAG,AES.block_size))
    print(iv.hex() + ct.hex())
    logging.info(json.dumps({
        "ct": ct.hex(),
        'iv': iv.hex(),
        "B": hex(B)[2:],
        "A": hex(A)[2:],
        "p": hex(p)[2:]
    }))

with open("strong_primes",'r') as f:
    primes = [int(p.strip(),16) for p in f]
authenticate(primes)