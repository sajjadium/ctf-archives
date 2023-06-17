from Crypto.Util.number import *
from hashlib import sha256
import os
import signal

BITS = 512

def POW():
    b = os.urandom(32)
    print(f"b = ??????{b.hex()[6:]}")
    print(f"SHA256(b) = {sha256(b).hexdigest()}")
    prefix = input("prefix > ")
    b_ = bytes.fromhex(prefix + b.hex()[6:])
    return sha256(b_).digest() == sha256(b).digest()

def generate_server_key():
    while True:
        p = getPrime(1024)
        q = getPrime(1024)
        e = 0x10001
        if (p-1) % e == 0 or (q-1) % e == 0:
            continue
        d = pow(e, -1, (p-1)*(q-1))
        n = p*q
        return e, d, n

# Generate N = (p1+p2) * (q1+q2) where p2 and q2 are shares chosen by the client
def generate_shared_modulus():
    SMALL_PRIMES = [2, 3, 5, 7, 11, 13]
    print(f"{SERVER_N = }")
    print(f"{SERVER_E = }")

    p1_remainder_candidates = {}
    q1_remainder_candidates = {}    
    # We prevent p1+p2 is divided by small primes
    # by asking the client for a possible remainders of p1
    for prime in SMALL_PRIMES:
        remainder_candidates = set(map(int, input(f"Candidates of p1 % {prime} > ").split()))
        assert len(remainder_candidates) == (prime+1) // 2, f"[-] wrong candidates for {prime}"
        p1_remainder_candidates[prime] = remainder_candidates
    
    while True:
        p1 = bytes_to_long(os.urandom(BITS // 8))        
        for prime in SMALL_PRIMES:
            if p1 % prime not in p1_remainder_candidates[prime]:
                break
        else:
            break
    
    # and same goes for q1
    for prime in SMALL_PRIMES:
        remainder_candidates = set(map(int, input(f"Candidates of q1 % {prime} > ").split()))
        assert len(remainder_candidates) == (prime+1) // 2, f"[-] wrong candidates for {prime}"
        q1_remainder_candidates[prime] = remainder_candidates
    
    while True:
        q1 = bytes_to_long(os.urandom(BITS // 8))
        
        for prime in SMALL_PRIMES:
            if q1 % prime not in q1_remainder_candidates[prime]:
                break
        else:
            break

    p1_enc = pow(p1, SERVER_E, SERVER_N)
    q1_enc = pow(q1, SERVER_E, SERVER_N)    

    print(f"{p1_enc = }")
    print(f"{q1_enc = }")
    X = list(map(int, input("X > ").split()))
    assert len(X) == 12
    
    N = (p1*q1 + sum(pow(x, SERVER_D, SERVER_N) for x in X)) % SERVER_N
    assert N.bit_length() >= 1024, f"[-] too short.., {N.bit_length()}"

    print(f"{N = }")
    
    return p1, q1, N

# check whether N is a product of two primes
def N_validity_check(p1, q1, N):
    for _ in range(20):
        b = bytes_to_long(os.urandom(2 * BITS // 8))
        print(f"{b = }")
        client_digest = input("Client digest > ")
        server_digest = sha256(long_to_bytes(pow(b, N+1-p1-q1, N))).hexdigest()
        if server_digest != client_digest:
            print("N is not a product of two primes I guess..")
            return False
        else:
            print("good!")
     
    return True

if not POW():
    exit(-1)

signal.alarm(60)
SERVER_E, SERVER_D, SERVER_N = generate_server_key()
p1, q1, N = generate_shared_modulus()
if not N_validity_check(p1, q1, N):
    exit(-1)

FLAG = open("flag", 'rb').read()
FLAG += b'\x00' + os.urandom(128 - 2 - len(FLAG))
FLAG_ENC = pow(bytes_to_long(FLAG), 0x10001, N)

print(f"{FLAG_ENC = }")

