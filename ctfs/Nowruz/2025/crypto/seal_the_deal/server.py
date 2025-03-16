from math import gcd
from Crypto.Util.number import getPrime, inverse
from random import randint
import secrets
import time

with open("flag.txt") as f:
    flag = f.readline()

class Paillier:
    def __init__(self, bits):
        self.bits = bits
        self.pub, self.priv = self.keygen()

    def lcm(self, a, b):
        return a * b // gcd(a, b)

    def keygen(self):
        while True:
            p = getPrime(self.bits)
            q = getPrime(self.bits)
            if p != q:
                break
        n = p * q
        Lambda = self.lcm(p - 1, q - 1)  
        g = n + 1  
        mu = inverse(Lambda, n) 
        return ((n, g), (Lambda, mu))

    def encrypt(self, m):
        (n, g) = self.pub
        n_sq = n * n
        while True:
            r = randint(1, n - 1)
            if gcd(r, n) == 1:
                break
        c = (pow(g, m, n_sq) * pow(r, n, n_sq)) % n_sq
        return c

    def decrypt(self, c):
        (n, g) = self.pub
        (Lambda, mu) = self.priv
        n_sq = n * n
        x = pow(c, Lambda, n_sq)  
        m = (((x - 1) // n) * mu) % n  
        return m

    def get_keys(self):
        return self.pub, self.priv

if __name__ == "__main__":

    print("Welcome to the Secure Gate Challenge!")
    paillier = Paillier(256)
    pub, priv = paillier.get_keys()
    print('(n,g)=', pub)
    nums = [secrets.randbits(16) for _ in range(4)]
    res = (nums[0] + nums[1]) + (nums[2] - nums[3])

    ciphers = [paillier.encrypt(i) for i in nums] 
    print('c1 =', ciphers[0])
    print('c2 =', ciphers[1])
    print('c3 =', ciphers[2])
    print('c4 =', ciphers[3])

    try:
        start_time = time.time()
        pass_code = int(input("Can you open the gate? If so, insert the passcode fast: "))
        if time.time() - start_time > 60:  
            print("Too slow! Time's up!")
            exit()
        pass_decode = paillier.decrypt(pass_code)
        if res == pass_decode:
            print(f"Wow! You opened it, The flag is: {flag}")
        else:
            print("Nope, Maybe next time :(")
    except Exception as e:
        print("Invalid input or error occurred:", str(e))
        exit()
