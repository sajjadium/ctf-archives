import os
from Crypto.Util.number import bytes_to_long, getPrime

from secret import FLAG

def main():
    F = bytes_to_long(FLAG)
    
    N = getPrime(1024)
    
    K1 = bytes_to_long(os.urandom(128))
    K2 = bytes_to_long(os.urandom(128))
    
    C1 = (F + K1) % N
    C2 = (K1 + K2) % N
    C3 = (K2 + F) % N
    
    print(f"N = {N}")
    print(f"C1 = {C1}")
    print(f"C2 = {C2}")
    print(f"C3 = {C3}")

if __name__ == "__main__":
    main()
