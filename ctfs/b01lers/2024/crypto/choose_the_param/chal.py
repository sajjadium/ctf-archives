#!/usr/bin/python3
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime
import os
from secret import flag

padded_flag = os.urandom(200) + flag + os.urandom(200)
m = bytes_to_long(padded_flag)

def chal():
    print("""Choose your parameter
Enter the bit length of the prime!
I'll choose two prime of that length, and encrypt the flag using rsa.
Try decrypt the flag!    
""")
    while True:
        bits = input("Enter the bit length of your primes> ")
        try:
            bit_len = int(bits)
        except:
            print("please enter a valid intergar")
            continue

        p1 = getPrime(bit_len)
        p2 = getPrime(bit_len)

        n = p1 * p2
        e = 65537
        c = pow(m, e, n)
        print(f"n = {n:x}")
        print(f"e = {e:x}")
        print(f"c = {c:x}")

if __name__ == "__main__":
    chal()
