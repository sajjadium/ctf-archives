from sage.all import *
from hashlib import sha256 as sha
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from secrets import token_bytes
from time import time


# preshared secret
preshared_secret = token_bytes(16)

# generate a strong prime
def strong_prime(bits):
    while True:
        p = random_prime(2**bits)
        q = (p - 1)//2
        if is_prime(q):
            return p
        
p = strong_prime(256)

# order of the subgroup
q = (p - 1)//2
# cyclic subgroup of quadratic residues 
g1 = pow(randint(2, p - 1), 2, p)
g2 = pow(randint(2, p - 1), 2, p)

assert pow(g1, q, p) == 1 and pow(g2, q, p) == 1 and g1 != g2

print(f"p = {p}\nq = {q}\ng1 = {g1}\ng2 = {g2}")

def hash(inputs):
    if not hasattr(inputs, "__iter__"):
        m = inputs
    else:
        m = "".join(map(str, inputs)).encode()
    return int(sha(m).hexdigest(), 16) % q

with open("flag") as f:
    flag = f.read().strip()

# private key
# I dont trust the PRNG on this machine
x1 = hash([preshared_secret, flag, "x1"])
x2 = hash([preshared_secret, flag, "x2"])

# public key
Y = (pow(g1, x1, p) * pow(g2, x2, p)) % p

print(f"Y = {Y}")

def sign(m):
    r = hash([m, x1, x2, time()])

    # add some untrusted entropy
    entropy = randint(1, 2 ** 250)
    
    l = entropy.bit_length()
    a = entropy & ((1 << ((l // 2) - 1)) - 1)
    b = entropy >> ((l // 2) - 1)

    r1 = (r + a) % q
    r2 = (r + b) % q

    R = (pow(g1, r1, p) * pow(g2, r2, p)) % p

    h = hash([m, R])
    
    s1 = (r1 + x1*h) % q
    s2 = (r2 + x2*h) % q
    
    return s1, s2, R

def verify(m, s1, s2, R):
    h = hash([m, R])
    return (pow(g1, s1, p) * pow(g2, s2, p)) % p == (R * pow(Y, h, p)) % p

assert verify("hello", *sign("hello"))

def encrypt(m):
    key = hash([(x1 - x2) % q]).to_bytes(32, "big")
    cipher = AES.new(key, AES.MODE_CBC)
    ct = cipher.encrypt(pad(m, 16))
    iv = cipher.iv
    
    return iv.hex() + ct.hex() 

print("")

m1 = "Hi! Can you store the encrypted flag for me for a second? I will need it later."
sig1 = sign(m1)
print(f"MESSAGE\nA:>{m1}\nSIG\n({sig1[0]},{sig1[1]},{sig1[2]})\n")

m2 = "Here's the flag: " + encrypt(flag.encode())
sig2 = sign(m2)

print(f"MESSAGE\nA:>{m2}\nSIG\n({sig2[0]},{sig2[1]},{sig2[2]})\n")
