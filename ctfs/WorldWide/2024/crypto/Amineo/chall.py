from secrets import randbits
from hashlib import sha256
import os

flag = os.getenv("flag", "wwf{<REDACTED>}").encode()
assert len(flag) == 32

p = 0xffffffffffffffffffffffffffffff53
Nr = 4

bSEED = b"AMINEO"
A = int.from_bytes(sha256(b"A" + bSEED).digest(), "big") % p
B = int.from_bytes(sha256(b"B" + bSEED).digest(), "big") % p

Ci = [int.from_bytes(sha256(b"C" + bSEED + str(r).encode()).digest(), "big") % p for r in range(Nr)]
Di = [int.from_bytes(sha256(b"D" + bSEED + str(r).encode()).digest(), "big") % p for r in range(Nr)]
Ei = [int.from_bytes(sha256(b"E" + bSEED + str(r).encode()).digest(), "big") % p for r in range(Nr)]
Fi = [int.from_bytes(sha256(b"F" + bSEED + str(r).encode()).digest(), "big") % p for r in range(Nr)]
Gi = [int.from_bytes(sha256(b"G" + bSEED + str(r).encode()).digest(), "big") % p for r in range(Nr)]
Hi = [int.from_bytes(sha256(b"H" + bSEED + str(r).encode()).digest(), "big") % p for r in range(Nr)]

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

class Amineo:
    def __init__(self, nr):
        self.nr = nr
        self.k = pow(3, -1, p - 1)
    
    def H(self, S):
        x, y = S
        x += A*y**2
        y += pow(x, self.k, p)
        x += B*y

        return x % p, y % p

    def M(self, S, r):
        x, y = S
        return Ci[r]*x + Di[r]*y + Ei[r] % p, Fi[r]*x + Gi[r]*y + Hi[r] % p

    def encrypt(self, S):
        Se = S.copy()
        for r in range(self.nr):
            Se = self.H(self.M(Se, r))

        return list(Se)

if __name__ == "__main__":
    print("I dont trust you but I guess you don't either...")

    try:
        user_B = bytes.fromhex(input("Give me 2 RANDOM blocks of 16 bytes (hex) >"))
        assert len(user_B) == 32
    except:
        print("I KNEW YOUD TRY TO CHEAT IF I GAVE YOU ANY CONTROL !!!")
        print("GET OUT OF HERE !!!")
        exit()

    S = [int.from_bytes(user_B[i:i+16], "big") % p for i in range(0, len(user_B), 16)]

    print("I dont trust you I'll add my part ...")
    tamper_idx = randbits(1)
    S[tamper_idx] *= randbits(128) % p

    enc = Amineo(Nr)
    OTP = enc.encrypt(S)

    print("Just to be sure I mean ... More random never hurts right ? :) ")
    OTP[0] *= randbits(128)
    OTP[1] *= randbits(128)
    OTP[0] %= p
    OTP[1] %= p

    OPTb = b"".join(int.to_bytes(OTP[i], 16, "big") for i in range(2))
    print("Here you go... :", xor(flag, OPTb).hex())
