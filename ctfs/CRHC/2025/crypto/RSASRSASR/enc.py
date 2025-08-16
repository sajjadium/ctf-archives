import random
from math import prod
from Crypto.Util.number import getPrime, bytes_to_long

def generate_prime_from_byte(byte_val):
    assert 0 <= byte_val <= 255
    r = random.Random()
    r.seed(byte_val)
    return getPrime(512, randfunc=r.randbytes)

def main():
    FLAG = open("flag.txt", "rb").read().strip()
    primes = [generate_prime_from_byte(b) for b in FLAG]
    
    N = prod(primes)
    
    e = 0x10001
    
    m = bytes_to_long(FLAG)
    c = pow(m, e, N)
    
    print(f"N = {hex(N)}")
    print(f"c = {hex(c)}")

if __name__ == "__main__":
    main()
