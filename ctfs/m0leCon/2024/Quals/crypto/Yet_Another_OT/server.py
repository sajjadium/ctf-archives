import random
from hashlib import sha256
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

random = random.SystemRandom()


def jacobi(a, n):
    if n <= 0:
        raise ValueError("'n' must be a positive integer.")
    if n % 2 == 0:
        raise ValueError("'n' must be odd.")
    a %= n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    if n == 1:
        return result
    else:
        return 0


def sample(start, N):
    while jacobi(start, N) != 1:
        start += 1
    return start


class Challenge:
    def __init__(self, N):
        assert N > 2**1024
        assert N % 2 != 0
        self.N = N
        self.x = sample(int.from_bytes(sha256(("x"+str(N)).encode()).digest(), "big"), N)
        ts = []
        tts = []
        for _ in range(128):
            t = random.randint(1, self.N)
            ts.append(t)
            tts.append(pow(t, N, N))
        print(json.dumps({"vals": tts}))
        self.key = sha256((",".join(map(str, ts))).encode()).digest()

    def one_round(self):
        z = sample(random.randint(1, self.N), self.N)
        r0 = random.randint(1, self.N)
        r1 = random.randint(1, self.N)

        m0, m1 = random.getrandbits(1), random.getrandbits(1)

        c0 = (r0**2 * (z)**m0) % self.N
        c1 = (r1**2 * (z*self.x)**m1) % self.N

        print(json.dumps({"c0": c0, "c1": c1}))
        data = json.loads(input())
        v0, v1 = data["m0"], data["m1"]
        return v0 == m0 and v1 == m1
    
    def send_flag(self, flag):
        cipher = AES.new(self.key, AES.MODE_ECB)
        ct = cipher.encrypt(pad(flag.encode(), 16))
        print(ct.hex())


FLAG = os.environ.get("FLAG", "ptm{test}")

def main():
    print("Welcome to my guessing game!")
    N = int(input("Send me a number: "))
    chall = Challenge(N)
    for _ in range(128):
        if not chall.one_round():
            exit(1)
    chall.send_flag(FLAG)


if __name__ == "__main__":
    main()