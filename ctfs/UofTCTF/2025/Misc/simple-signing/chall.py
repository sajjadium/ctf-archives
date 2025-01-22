from Crypto.Util.number import getPrime
from secrets import FLAG
ADMIN = b'adminTokenPlsNoSteal'


def sign(n: int, d: int, m: bytes):
    if m == ADMIN:
        print("no no")
        exit(0)
    
    h = hash(tuple(m))
    return pow(h, d, n)

def verify(n: int, e: int, m: bytes, s: int):
    h = hash(tuple(m))
    return pow(s, e, n) == h

if __name__ == "__main__":
    p, q = getPrime(1024), getPrime(1024)
    e = 0x10001
    n = p*q
    d = pow(e, -1, (p-1)*(q-1))

    print("""1. sign a message
2. get flag""")
    while True:
        inp = input("> ")
        if int(inp) == 1:
            msg = bytes.fromhex(input("Message to sign (in hex): "))
            print("Signature:", sign(n, d, msg))
        else:
            sig = int(input("Give signature of admin token: "))
            if verify(n, e, ADMIN, sig):
                print("Congratz!!")
                print(FLAG)
                exit(0)
            else:
                print("You are not the admin")
                exit(0)