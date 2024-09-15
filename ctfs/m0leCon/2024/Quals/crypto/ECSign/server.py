from Crypto.PublicKey.ECC import EccPoint
from Crypto.Random import random
import hashlib
import json
import os

FLAG = os.environ.get("FLAG", "ptm{test}")

p = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
Gx = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
Gy = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
q = 0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551
G = EccPoint(Gx, Gy)

N = 32
T = 64
B = 4

bases = [random.randint(1, q-1) for _ in range(N)]

def action(pub, priv):
    res = 1
    for li, ei in zip(bases, priv):
        res = (res * pow(li, ei, q)) % q
    Q = res * pub
    return Q

def keygen():
    sk = [random.randint(-B, B) for _ in range(N)]
    pk = action(G, sk)
    return (sk, pk)

def sub(a, b):
    return [x-y for x,y in zip(a, b)]

def sign(msg, sk):
    fs = []
    Ps = []
    cnt = 0
    while cnt < T:
        f = [random.randint(-(N*T+1)*B, (N*T+1)*B) for _ in range(N)]
        b = sub(f, sk)
        vec = [-N*T*B <= bb <= N*T*B for bb in b]
        if all(vec):
            P = action(G, f)
            fs.append(f)
            Ps.append((P.x,P.y))
            cnt += 1
    s = ",".join(map(str, Ps)) + "," + msg
    h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
    outs = []
    for i in range(T):
        b = (h>>i) & 1
        if b:
            outs.append((b, sub(fs[i], sk)))
        else:
            outs.append((b, fs[i]))
    return outs

def verify(msg, sigma, pk):
    Ps = []
    for i in range(T):
        if sigma[i][0]:
            start = pk
        else:
            start = G
        end = action(start, sigma[i][1])
        Ps.append((end.x, end.y))
    s = ",".join(map(str, Ps)) + "," + msg
    h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
    for i in range(T):
        b = (h>>i) & 1
        if b != sigma[i][0]:
            return False
    return True


def menu():
    print("Choose an action")
    print("1. Sign a message")
    print("2. Get the flag")
    print("3. Quit")
    return int(input(">"))

def main():
    print("Let's sign some messages!")

    FLAG_MSG = "gimmetheflag"

    sk, pk = keygen()

    print(bases)
    print(pk.x, pk.y)

    while True:
        choice = menu()
        if choice == 1:
            m = input("The message to sign: ")
            if m == FLAG_MSG:
                print("Lol nope")
                exit(0)
            signature = sign(m, sk)
            print(json.dumps(signature))
        elif choice == 2:
            sigma = json.loads(input("Give me a valid signature: "))
            if verify(FLAG_MSG, sigma, pk):
                print(FLAG)
        else:
            break


if __name__ == "__main__":
    main()

