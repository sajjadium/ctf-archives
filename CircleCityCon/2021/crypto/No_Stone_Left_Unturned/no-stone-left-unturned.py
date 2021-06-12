from gmpy2 import next_prime, is_prime
import random, os, sys

if __name__ == "__main__":
    random.seed(os.urandom(32))
    p = next_prime(random.randrange((1<<1024), (1<<1024) + (1<<600)))
    pp = (p * 7) // 11
    q = next_prime(random.randrange(pp - (1<<520), pp + (1 << 520)))
    with open(sys.argv[1], "rb") as f:
        flag = int.from_bytes(f.read(), "big")
    assert is_prime(p)
    assert is_prime(q)
    N = p * q
    assert flag < N
    e = 0x10001
    c = pow(flag, e, N)
    with open("out.txt", "w") as f:
        f.write(f"N = {hex(N)}\n")
        f.write(f"e = {hex(e)}\n")
        f.write(f"c = {hex(c)}\n")

