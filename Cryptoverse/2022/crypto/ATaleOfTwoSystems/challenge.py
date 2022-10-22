from Crypto.Util.number import *
from secret import flag

NBITS = 1024

def system_one(m: bytes):
    a, b = [getRandomNBitInteger(NBITS) for _ in range(2)]
    p = getPrime(2 * NBITS)
    q = getPrime(NBITS // 2)
    g = inverse(a, p) * q % p

    ct = (b * g + bytes_to_long(m)) % p

    print(f"p = {p}")
    print(f"g = {g}")
    print(f"ct = {ct}\n")

def system_two(m: bytes):
    p, q = [getPrime(NBITS // 2) for _ in range(2)]
    n = p * q
    e = 0x10001
    ct = pow(bytes_to_long(m), e, n)

    print(f"n = {n}")
    print(f"e = {e}")
    print(f"ct = {ct}")
    
    # what if q is reversed?
    q = int('0b' + ''.join(reversed(bin(q)[2:])), 2)
    hint = p + q - 2 * (p & q)
    print(f"hint = {hint}")

def main():
    print("When you combine two insecure systems, you get an insecure system. (Cryptoverse CTF, 2022)")
    print("[+] System 1")
    system_one(flag[:len(flag) // 2])
    print("[+] System 2")
    system_two(flag[len(flag) // 2:])

if __name__ == "__main__":
    main()