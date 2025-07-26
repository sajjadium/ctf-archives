import os, time, signal
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_string
from random import SystemRandom

G = SECP256k1.generator
n = SECP256k1.order
BITS = 64

def sign_with_nonce(sk, message, nonce):
    e = int.from_bytes(sha256(message).digest(), 'big')
    R = nonce * G
    r = R.x() % n
    if r == 0: raise ValueError("Invalid nonce: r == 0")

    k_inv = pow(nonce, -1, n)
    s = (k_inv * (e + r * sk)) % n
    if s == 0: raise ValueError("Invalid signature: s == 0")

    return (r, s, R.y() % 2)

def banner():
    print("""
Welcome to BULLMAD -- The premium BPN solution!
Here you can redeem your 1, 3, 6 or 12 month codes and add time to your BPN account.
The codes are signatures, and look like these DEMO messages:
    """.strip())
    signal.alarm(60)

if __name__ == "__main__":
    banner()
    rnd = SystemRandom()
    nonce = rnd.randint(1, n - 1)
    demo_accounts = sorted((rnd.getrandbits(BITS), length) for length in [30, 180])
    sk = int.from_bytes(os.urandom(32), "big")
    pk = SigningKey.from_secret_exponent(sk, curve=SECP256k1, hashfunc=sha256).get_verifying_key()

    print(f"My pubkey is {pk}")
    
    for i,(account_id,length) in enumerate(demo_accounts):
        message = f"DEMO Account expires at {time.time()+86400*length:.0f}"
        r, s, v = sign_with_nonce(sk, message.encode(), (nonce + account_id)%(n - 1))
        print(f"m{i+1} = '{message}'")
        print(f"r{i+1} = {hex(r)}")
        print(f"s{i+1} = {hex(s)}")
        print(f"v{i+1} = {hex(v)}")

    message = f"Account expires at {time.time()+86400*360:.0f}"
    print(f"Now give me a signature for a 1 year non-demo account: '{message}'")
    r = int(input("r = "))
    s = int(input("s = "))

    try:
        if pk.verify(sigencode_string(r,s,n), message.encode(), hashfunc=sha256):
            print(open("flag.txt").read())
    except:
        print("Bad signature, are you sure you entered it correctly?")