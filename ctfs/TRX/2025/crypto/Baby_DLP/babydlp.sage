from hashlib import sha256
from binascii import crc32
import re
from Crypto.Util.number import bytes_to_long, long_to_bytes
from random import randint

flag=open("flag.txt", "r").read().strip()
assert re.match(r"TRX\{[a-z_]{39}\}", flag)

E = EllipticCurve(GF(0x05ab035976b887b505bfcc20df74d9ab3d4a50cb87f5cede0d), [0x04ae328d15285fa70cf60749cf41cf14e1a316651fe8ce3b23, 0x03c7abc7899e550ba2eaeb5be64da31af90073a08c1d3e0215])

G = E(
    0x570f7cc8830e8cbfd1d8890fac962275f1553b11e4f3e2af7,
    0x9d18b5cee48c50824741c5f8fdf1cd8cbf9fc3dd200f2fe9
)

d = bytes_to_long(flag.encode())
Q = d*G


def sign(msg, d):
    h = int(sha256(msg).hexdigest(),16)
    
    # double nonce = impossible to guess
    k1 = crc32(msg + str(randint(1, 2**32)).encode())
    k2 = crc32(msg + str(randint(1, 2**32)).encode())
    R = (k1+k2)*G
    s = (h*k2 + d*R[0])/k1
    return R, s

def verify(msg, R, s, Q):
    # I never remember how to do this properly
    return False

print("""Welcome to another super usefull signature service that can only sign messages!""")
print("Here is your public key:")
print(f"Q = ({Q[0]}, {Q[1]})")
print("I don't know what you will use it for, but as it's a public key, it's public!")

try:
    while True:
        print("""What do you want to do?
1 Sign a message
2 Verify a signature
* Exit""")
        choice = input("> ")
        if choice == "1":
            msg = input("Enter the message you want to sign: ").encode()
            R, s = sign(msg, d)
            print(f"Here is the signature:")
            print(f"R = ({R[0]}, {R[1]})")
            print(f"s = {s}")
        elif choice == "2":
            print("Sorry, I don't know how to do this.")
        else:
            print("Goodbye!")
            break
except Exception:
    pass
