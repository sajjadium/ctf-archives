import random
import hashlib
import json
import os

ls = list(prime_range(3,117))
p = 4 * prod(ls) - 1
base = 0
N = len(ls)
T = 30
B = 5

R.<t> = GF(p)[]

#Thanks to Lorenz Panny @yx7 for the CSIDH code! :D
def montgomery_coefficient(E):
    a,b = E.short_weierstrass_model().a_invariants()[-2:]
    r, = (t**3 + a*t + b).roots(multiplicities=False)
    s = sqrt(3*r**2 + a)
    return -3 * (-1)**is_square(s) * r / s


def csidh(pub, priv):
    E = EllipticCurve(GF(p), [0, int(pub), 0, 1, 0])
    assert (p+1) * E.random_point() == E(0)
    for es in ([max(0,+e) for e in priv], [max(0,-e) for e in priv]):
        while any(es):
            x = GF(p).random_element()
            try: P = E.lift_x(x)
            except ValueError: continue
            k = prod(l for l,e in zip(ls,es) if e)
            P *= (p+1) // k
            for i,(l,e) in enumerate(zip(ls,es)):
                if not e: continue
                k //= l
                Q = k*P
                if Q == 0: continue
                phi = E.isogeny(Q)
                E,P = phi.codomain(), phi(P)
                es[i] -= 1
        E = E.quadratic_twist()
    return int(montgomery_coefficient(E))


def keygen():
    sk = [random.randint(-B, B) for _ in range(N)]
    pk = csidh(base, sk)
    return (sk, pk)


def sub(a, b):
    return [x-y for x,y in zip(a, b)]


def sign(msg, sk):
    fs = []
    Es = []
    for i in range(T):
        f = [random.randint(-B, B) for _ in range(N)]
        E = csidh(base, f)
        fs.append(f)
        Es.append(E)
    s = ",".join(map(str, Es)) + "," + msg
    h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
    outs = []
    for i in range(T):
        b = (h>>i) & 1
        if b:
            outs.append({"bit": int(b), "vec": [int(x) for x in sub(fs[i], sk)]})
        else:
            outs.append({"bit": int(b), "vec": [int(x) for x in fs[i]]})
    return outs


def verify(msg, sigma, pk):
    Es = []
    for i in range(T):
        if sigma[i]["bit"]:
            start = pk
        else:
            start = base
        Es.append(csidh(start, sigma[i]["vec"]))
    s = ",".join(map(str, Es)) + "," + msg
    h = int.from_bytes(hashlib.sha256(s.encode()).digest(), "big")
    for i in range(T):
        b = (h>>i) & 1
        if b != sigma[i]["bit"]:
            return False
    return True


assert "FLAG" in os.environ
FLAG = os.environ["FLAG"]


def menu():
    print("1. Get a signature")
    print("2. Get the flag")
    print("3. Quit")
    return int(input("> "))

def main():
    sk, pk = keygen()
    print(f"Server's public key is: {pk}")

    while True:
        choice = menu()
        if choice == 1:
            print("What's your message?")
            msg = input()
            assert msg.isalnum()
            assert "flag" not in msg.lower()
            sigma = sign(msg, sk)
            print(json.dumps({"msg": msg, "signature": sigma}))
        elif choice == 2:
            print("Lemme check your signature")
            data = json.loads(input())
            msg = data["msg"]
            sigma = data["signature"]
            if not verify(msg, sigma, pk):
                print("Invalid signature")
                exit(1)
            if msg == "gimmetheflag":
                print(FLAG)
        else:
            exit(0)


if __name__ == "__main__":
    main()
