import sys
import os

sys.path.insert(1, "SQISign-SageMath")

from SQISign import SQISign
from setup import Fp4

z4 = Fp4.gens()[0]

FLAG = os.environ.get("FLAG", "flag{test_flag}")

with open("public_key", "rb") as f:
    EA = loads(f.read())

verifier = SQISign()

msg = b"give me the flag"

# Need the exact curve E1
print("Give a4 coefficient")
a40 = int(input("a40: "))
a41 = int(input("a41: "))
a42 = int(input("a42: "))
a43 = int(input("a43: "))
a4 = z4^3*a43 + z4^2*a42 + z4*a41 + a40

print("Give a6 coefficient")
a60 = int(input("a60: "))
a61 = int(input("a61: "))
a62 = int(input("a62: "))
a63 = int(input("a63: "))
a6 = z4^3*a63 + z4^2*a62 + z4*a61 + a60


E1 = EllipticCurve(Fp4, [a4, a6])
S = input("S: ")
deg_sigma = int(input("deg_sigma: "))

phi_ker = verifier.challenge_from_message(E1, msg)

if verifier.verify_response(EA, E1, S, phi_ker, deg_sigma=deg_sigma):
    print(FLAG)
else:
    print("Nope")
