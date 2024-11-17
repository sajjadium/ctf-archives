from Crypto.Util.number import *
import signal

def timeout_handler(signum, frame):
    print("Secret key expired")
    exit()

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)

FLAG = "INTIGRITI{fake_flag}"
SIZE = 32

class Alice:
    def __init__(self):
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.n = self.p*self.q
        self.e = 0x10001
    
    def public_key(self):
        return self.n,self.e
    
    def decrypt_key(self, ck):
        phi = (self.p-1)*(self.q-1)
        d = inverse(e, phi)
        self.k = pow(ck, d, n)

class Bob:
    def __init__(self):
        self.k = getRandomNBitInteger(SIZE)

    def key_exchange(self, n, e):
        return pow(self.k, e, n)

alice = Alice()
bob = Bob()

n,e = alice.public_key()
print("Public key from Alice :")
print(f"{n=}")
print(f"{e=}")

ck = bob.key_exchange(n, e)
print("Bob sends encrypted secret key to Alice :")
print(f"{ck=}")

alice.decrypt_key(ck)
assert(alice.k == bob.k)

try:
    k = int(input("Secret key ? "))
except:
    exit()

if k == bob.k:
    print(FLAG)
else:
    print("That's not the secret key")
