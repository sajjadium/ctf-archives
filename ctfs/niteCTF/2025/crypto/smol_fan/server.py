from hashlib import sha256
from ecdsa import VerifyingKey, SECP256k1
from gmpy2 import is_prime
import os
import sympy
import secrets  

FLAG_MESSAGE = b"gimme_flag"
FLAG = os.getenv("flag","nite{fake_flag}")

curve = SECP256k1
G = curve.generator
n = curve.order

d = secrets.randbelow(n) 
Q = d * G
vk = VerifyingKey.from_public_point(Q, curve=SECP256k1)

def ecdsa_sign(message: bytes):
    while True:
        z = int.from_bytes(sha256(message).digest(),"big") % n
        k = secrets.randbelow(2**200 - 1) + 1 
        R = k * G
        r = R.x() % n
        if r == 0 or is_prime(r) == 0:
            continue
        k_inv = pow(k,-1,n)
        s = (k_inv * (z + r*d)) % n
        if s == 0 or is_prime(s) == 0:
            continue
        
        m = r*s
        a = pow(10 + r,11,m)
        b = pow(s**2 + 10,r,m)

        return m,a,b
    
def ecdsa_verify(message: bytes, r: int, s: int) -> bool:
    if not (1 <= r < n and 1 <= s < n):
        return False
    z = int.from_bytes(sha256(message).digest(),"big") % n
    w = pow(s,-1,n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    X = u1 * G + u2 * Q
    x = X.x() % n
    return x == r

def get_pubkey():
    print("Public key (uncompressed):")
    print(f"Qx = {Q.x()}")
    print(f"Qy = {Q.y()}\n")

def cmd_sign():
    m_hex = input("Enter message as hex: ").strip()
    try:
        msg = bytes.fromhex(m_hex)
    except ValueError:
        print("Invalid hex.\n")
        return

    if msg == FLAG_MESSAGE:
        print("THATS NOT ALLOWED.\n")
        return
    
    m,a,b = ecdsa_sign(msg)  
    print(f"m = {m}")
    print(f"a = {a}\n")
    print(f"b = {b}\n")

def claim():
    print("Submit a signature for the flag.")
    try:
        r_str = input("Enter r: ").strip()
        s_str = input("Enter s: ").strip()
        r = int(r_str)
        s = int(s_str)
    except ValueError:
        print("Invalid integers.\n")
        return

    if ecdsa_verify(FLAG_MESSAGE, r, s):
        print(FLAG)
    else:
        print("Invalid signature.\n")

def main():
    print("Menu:")
    print("  1) Get public key")
    print("  2) Sign a message")
    print("  3) Submit claim for the flag")
    print("  4) Quit")

    while True: 
        choice = input("> ").strip()

        if choice == "1":
            get_pubkey()
        elif choice == "2":
            cmd_sign()
        elif choice == "3":
            claim()
        elif choice == "4":
            print("Bye!")
            break
        else:
            print("Invalid choice.\n")

if __name__ == "__main__":
    main()



    


