from random import randint
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
import numpy as np

def get_b(n):
    b = []
    b.append(randint(2**(n-1), 2**n))
    for i in range(n - 1):
        lb = sum(b)
        found = False
        while not found:
            num = randint(max(2**(n + i), lb + 1), 2**(n + i + 1))
            if num > lb:
                found = True
                b.append(num)

    return b

def get_MW(b):
    lb = sum(b)
    M = randint(lb + 1, 2*lb)
    W = getPrime(int(1.5*len(b)))

    return M, W

def get_a(b, M, W):
    a_ = []
    for num in b:
        a_.append(num * W % M)
    pi = np.random.permutation(list(i for i in range(len(b)))).tolist()
    a = [a_[pi[i]] for i in range(len(b))]
    return a, pi


def enc(flag, a, n):
    bitstrings = []
    for c in flag:
        # c -> int -> 8-bit binary string
        bitstrings.append(bin(ord(c))[2:].zfill(8))
    ct = []
    for bits in bitstrings:
        curr = 0
        for i, b in enumerate(bits):
            if b == "1":
                curr += a[i]
        ct.append(curr)

    return ct

def dec(ct, a, b, pi, M, W, n):
    # construct inverse permuation to pi
    pii = np.argsort(pi).tolist()
    m = ""
    U = pow(W, -1, M)
    ct = [c * U % M for c in ct]
    for c in ct:
        # find b_pi(j)
        diff = 0
        bits = ["0" for _ in range(n)]
        for i in reversed(range(n)):
            if c - diff > sum(b[:i]):
                diff += b[i]
                bits[pii[i]] = "1"
        # convert bits to character
        m += chr(int("".join(bits), base=2))

    return m


def main():
    flag = 'uiuctf{I_DID_NOT_LEAVE_THE_FLAG_THIS_TIME}'

    # generate cryptosystem
    n = 8
    b = get_b(n)
    M, W = get_MW(b)
    a, pi = get_a(b, M, W)

    # encrypt
    ct = enc(flag, a, n)

    # public information
    print(f"{a =  }")
    print(f"{ct = }")

    # decrypt
    res = dec(ct, a, b, pi, M, W, n)

if __name__ == "__main__":
    main()
