import alice_secret
from pwn import *
import hashlib
from Crypto.Cipher import AES
from Crypto.Util import Padding

GENERATOR = 2
KEY_BYTES = 16
PRIME_BITS = 2048

def main(primes)->str:
    prc = process(['python3', 'server.py'])
    try:
        p = int(prc.recvline().decode('utf-8'),16)
        if p not in primes:
            raise ValueError(f"Server responded with invalid prime: {p}")
        A = pow(GENERATOR,alice_secret.a,p)
        prc.sendline(hex(A)[2:].encode('utf-8'))
        B = int(prc.recvline().decode('utf-8'),16)
        ct = bytes.fromhex(prc.recvline().decode('utf-8'))
        ss = pow(B,alice_secret.a,p)
        key = hashlib.sha256(ss.to_bytes(PRIME_BITS//8,'big')).digest()[:KEY_BYTES]
        cipher = AES.new(key,AES.MODE_CBC,iv=ct[:AES.block_size])
        return Padding.unpad(cipher.decrypt(ct[AES.block_size:]),AES.block_size).decode('utf-8')
    finally:
        prc.kill()

if __name__ == "__main__":
    with open("strong_primes",'r') as f:
        primes = set(map(lambda p: int(p.strip(),16),f))
        print(main(primes))