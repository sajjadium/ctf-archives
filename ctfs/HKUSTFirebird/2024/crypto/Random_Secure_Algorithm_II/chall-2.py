from Crypto.Util.number import getPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import signal
import hashlib
import os
import random

def tle_handler(*args):
    print('⏰')
    sys.exit(0)

class RSA:
    def __init__(self, n = 1024):
        p = getPrime(n // 2)
        q = getPrime(n // 2)
        self.n = p * q
        self.e = 0x10001
        self.d = pow(self.e, -1, (p - 1) * (q - 1))
    
    def encrypt(self, m):
        return pow(m, self.e, self.n)
    
    def decrypt(self, c):
        return pow(c, self.d, self.n)

def dot_mod(c1, c2, n):
    assert len(c1) == len(c2)
    return sum(i * j for i, j in zip(c1, c2)) % n

def main():

    signal.signal(signal.SIGALRM, tle_handler)
    signal.alarm(60)
    
    FLAG = os.environ.get('FLAG', 'firebird{***REDACTED***}').encode()
    secret = [os.urandom(8) for _ in range(10)]
    
    iv = os.urandom(16)
    enc_flag = iv + AES.new(key = hashlib.sha256(b''.join(secret)).digest(), mode = AES.MODE_CBC, iv = iv).encrypt(pad(FLAG, 16))
    print(f'🏁 {enc_flag.hex()}')

    rsa = RSA()
    print(f'📢 {hex(rsa.n)[2:]}')

    enc_secret = []
    for block in secret:
        enc_secret.append(rsa.encrypt(int.from_bytes(block, 'big')))
    enc_s = ':'.join(hex(c)[2:].rjust(1024 // 8 * 2, '0') for c in enc_secret)
    print(f'🔑 {enc_s}')



    ct = input('🔓 ').strip().replace('-', '').split(':')
    pt = [rsa.decrypt(int(c, 16)) for c in ct]

    weights = enc_secret
    random.shuffle(weights)

    res = dot_mod(pt, weights, rsa.n)
    print(f'🧾 {hex(res)[2:]}')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('😒')