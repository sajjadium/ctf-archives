from Crypto.Util.number import getPrime, isPrime, getRandomRange, inverse, long_to_bytes
from hashlib import sha256
import os
import secrets
import signal


def h1(s: bytes) -> int:
    return int(sha256(s).hexdigest()[:40], 16)

def h2(s: bytes) -> int:
    return int(sha256(s).hexdigest()[:50], 16)

# curl https://2ton.com.au/getprimes/random/2048
q = 10855513673631576111128223823852736449477157478532599346149798456480046295301804051241065889011325365880913306008412551904076052471122611452376081547036735239632288113679547636623259366213606049138707852292092112050063109859313962494299170083993779092369158943914238361319111011578572373690710592496259566364509116075924022901254475268634373605622622819175188430725220937505841972729299849489897919215186283271358563435213401606699495614442883722640159518278016175412036195925520819094170566201390405214956943009778470165405468498916560026056350145271115393499136665394120928021623404456783443510225848755994295718931
p = 2*q + 1

assert isPrime(p)
assert isPrime(q)

g = 3
flag = os.getenv("FLAG", "neko{nanmo_omoi_tsukanai_owari}")
x = getRandomRange(0, q)
y = pow(g, x, p)
salt = secrets.token_bytes(16)


def sign(m: bytes):
    z = h1(m)
    k = inverse(h2(long_to_bytes(x + z)), q)
    r = h2(long_to_bytes(pow(g, k, p)))
    s = (z + x*r) * inverse(k, q) % q
    return r, s


def verify(m: bytes, r: int, s: int):
    z = h1(m)
    sinv = inverse(s, q)
    gk = pow(g, sinv*z, p) * pow(y, sinv*r, p) % p
    r2 = h2(long_to_bytes(gk))
    return r == r2

# integrity check
r, s = sign(salt)
assert verify(salt, r, s)

signal.alarm(1000)


print("salt =", salt.hex())
print("p =", p)
print("g =", g)
print("y =", y)

while True:
    choice = input("[s]ign or [v]erify:").strip()
    if choice == "s":
        print("=== sign ===")
        m = input("m = ").strip().encode()
        if b"goma" in m:
            exit()

        r, s = sign(m + salt)
        # print("r =", r) #  do you really need?
        print("s =", s)

    elif choice == "v":
        print("=== verify ===")
        m = input("m = ").strip().encode()
        r = int(input("r = "))
        s = int(input("s = "))
        assert 0 < r < q
        assert 0 < s < q

        ok = verify(m + salt, r, s)
        if ok and m == b"hirake goma":
            print(flag)
        elif ok:
            print("OK")
            exit()
        else:
            print("NG")
            exit()

    else:
        exit()
