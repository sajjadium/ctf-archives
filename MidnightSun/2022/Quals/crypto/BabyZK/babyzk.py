#!/usr/bin/python3

from sys import stdin, stdout, exit
from secrets import randbelow
from gmpy import next_prime

from flag import FLAG


class BabyZK:

    def __init__(self, degree, nbits):
        self.p = self.__safeprime(nbits)
        self.degree = degree
        self.m = [randbelow(self.p-1) for i in range(self.degree)]
        self.g = 2 + randbelow(self.p-3)
        self.ctr = 0

    def __safeprime(self, nbits):
        stdout.write("Generating safeprime...")
        p = -1
        while True:
            q = next_prime(randbelow(2 * 2**nbits))
            p = 2*q + 1
            if p.is_prime():
                break
        return p

    def __eval(self, x: int) -> int:
        y = 0
        for a in self.m:
            y += y * x + a
        return y % (self.p-1)

    def prover(self, x: int) -> int:
        if self.ctr > self.degree + 1:
            raise Exception("Sorry, you are out of queries...")
        self.ctr += 1
        return int(pow(self.g, self.__eval(x), self.p))

    def verify(self, x: int, u: int):
        if not u < self.p or u < 0:
            raise Exception("Oof, this is not mod p...")
        if int(pow(self.g, self.__eval(x), self.p)) != u:
            raise Exception("No can do...")


bzk = BabyZK(15, 1024)

def prove():
    stdout.write("> ")
    stdout.flush()
    challenge = int(stdin.readline())
    stdout.write("%d\n" % bzk.prover(challenge))
    stdout.flush()

def verify():
    for i in range(100):
        challenge = randbelow(bzk.p)
        stdout.write("%d\n" % challenge)
        stdout.flush()
        response = int(stdin.readline())
        bzk.verify(challenge, response)
    stdout.write("%s\n" % FLAG)
    stdout.flush()

banner = lambda: stdout.write("""
1) Query the prover oracle.
2) Prove to verifier that you know the secret.
3) Exit.
""")

choices = {
    1: prove,
    2: verify,
    3: exit
}

banner()
stdout.flush()

while True:
    try:
        choice = stdin.readline()
        choices.get(int(choice))()
    except Exception as e:
        stdout.write("%s\n" % e)
        stdout.flush()
        exit()
