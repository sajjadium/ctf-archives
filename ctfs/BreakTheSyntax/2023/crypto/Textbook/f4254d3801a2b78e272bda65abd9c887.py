from Crypto.Util.number import getPrime, GCD, getRandomRange
from collections import namedtuple


with open('flag', 'r') as f:
    flag = f.read()

public = namedtuple('public', 'n g')
secret = namedtuple('secret', 'n phi mu')
sig = namedtuple('sig', 's1 s2')

b = 1024
p = getPrime(b)
q = getPrime(b)

assert p != q

n = p * q
phi = (p - 1) * (q - 1)
g = n + 1
mu = pow(phi, -1, n)

pk = public(n, g)
sk = secret(n, phi, mu)

# mask for additional security!!!
mask = getRandomRange(2 ** (n.bit_length() * 2 - 2), (2 ** (n.bit_length() * 2 - 1)))

def h(s: bytes) -> int:
    return int.from_bytes(s, 'big', signed=True)

def int_to_bytes(n: int) -> bytes:
    return n.to_bytes(n.bit_length() // 8 + 1, 'big', signed=True)

def encrypt(m: bytes, pk: public) -> bytes:
    n, g = pk
    r = getRandomRange(1, n)
    assert GCD(r, n) == 1
    mh = h(m)
    c = (pow(g, mh, n ** 2) * pow(r, n, n ** 2)) % (n ** 2)

    return pow(c, mask, n ** 2)

def sign(m: bytes, sk: secret) -> sig:
    n, phi, mi = sk
    mh = (h(m) * mask) % (n ** 2)
    d = pow(mh, phi, n ** 2)
    e = (d - 1) // n

    s1 = (e * mi) % n
    n_inv = pow(n, -1, phi)
    s2 = pow(mh * pow(g, -s1, n), n_inv, n)
    
    return sig(s1, s2)

def verify(m: bytes, sig: sig, pk: public) -> bool:
    s1, s2 = sig
    n, g = pk
    mh = (h(m) * mask) % (n ** 2)
    
    m_prim = pow(g, s1, n ** 2) * pow(s2, n, n ** 2) % (n ** 2)
    return m_prim == mh

if __name__=="__main__":
    flag_enc = encrypt(flag.encode(), pk)
    flag_enc = int_to_bytes(flag_enc)
    print("Hello to my signing service ^^\n")
    print("My public key:")
    print("n =", pk.n)
    print("g =", pk.g)
    print("\nHere, have flag. It's encrypted and masked anyways, so who cares.\n")
    print("flag =", (flag_enc.hex()), "\n")


    while True:
        print("What do you want to do?")
        print("[1] Sign something", "[2] Verify signature", "[3] Exit", sep="\n")

        function = input(">")

        if function == "1":
            message = bytes.fromhex(input("Give me something to sign!\n(hex)>"))
            signature = sign(message, sk)
            print(f"s1 = {signature.s1}\ns2 = {signature.s2}")
        if function == "2":
            message = bytes.fromhex(input("Message to verify\n(hex)>"))
            print("Signature:")
            signature = sig(int(input("s1:\n(int)>")), int(input("s2:\n(int)>")))
            if verify(message, signature, pk):
                print("verified!")
            else:
                print("not verified!")
        if function == "3":
            exit()


