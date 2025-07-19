#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from hashlib import sha256
from secrets import randbits
import os

FLAG = os.getenv('FLAG', 'DUCTF{FLAG_TODO}')

class TokenService: 
    def __init__(self):
        self.p = getPrime(512)
        self.q = getPrime(512)
        self.n = self.p * self.q
        self.n2 = self.n * self.n
        self.l = (self.p - 1) * (self.q - 1)
        self.g = self.n + 1
        self.mu = pow(self.l, -1, self.n)
        self.secret = os.urandom(16)

    def _encrypt(self, m):
        r = randbits(1024)
        c = pow(self.g, m, self.n2) * pow(r, self.n, self.n2) % self.n2
        return c

    def _decrypt(self, c):
        return ((pow(c, self.l, self.n2) - 1) // self.n) * self.mu % self.n

    def generate(self, msg):
        h = bytes_to_long(sha256(self.secret + msg).digest())
        return long_to_bytes(self._encrypt(h))

    def verify(self, msg, mac):
        h = sha256(self.secret + msg).digest()
        w = long_to_bytes(self._decrypt(bytes_to_long(mac)))
        return h == w[-32:]


def menu():
    print('1. Register')
    print('2. Login')
    return int(input('> '))


def main():
    ts = TokenService()
    print(ts.n)

    while True:
        choice = menu()
        if choice == 1:
            username = input('Username: ').encode()
            if b'admin' in username:
                print('Cannot register admin user')
                exit(1)
            msg = b'user=' + username
            mac = ts.generate(msg)
            print('Token:', (msg + b'|' + mac).hex())
        elif choice == 2:
            token = bytes.fromhex(input('Token: '))
            msg, _, mac = token.partition(b'|')
            if ts.verify(msg, mac):
                user = msg.rpartition(b'user=')[2]
                print(f'Welcome {user}!')
                if user == b'admin':
                    print(FLAG)
            else:
                print('Failed to verify token')
        else:
            exit(1)


if __name__ == '__main__':
    main()
