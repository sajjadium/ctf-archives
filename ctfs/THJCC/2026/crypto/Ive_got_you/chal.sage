from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hashlib
import os

ea, eb = 13, 7

p = 2**ea * 3**eb - 1
K.<i> = GF(p**2, modulus=x**2 + 1)

E0 = EllipticCurve(K, [0, 6, 0, 1, 0])

def get_isogeny_chain(E, l, e, secret):
    curr_E = E
    phis = []
    for i in range(e):
        P, Q = curr_E.torsion_basis(l**(e-i))
        kernel_pt = (P + secret * Q) * l**(e-i-1)
        phi = curr_E.isogeny(kernel_pt)
        phis.append(phi)
        curr_E = phi.codomain()
    return curr_E, phis

def push_point(phi_list, P):
    curr_P = P
    for phi in phi_list:
        curr_P = phi(curr_P)
    return curr_P

sa = randint(0, 2**ea - 1)
sb = randint(0, 3**eb - 1)

Ea, phis_a = get_isogeny_chain(E0, 2, ea, sa)
Eab, phis_b = get_isogeny_chain(Ea, 3, eb, sb)

P_pub = E0.random_element()
P_priv = push_point(phis_b, push_point(phis_a, P_pub))

shared_x = P_priv.xy()[0]
key = hashlib.sha256(str(shared_x).encode()).digest()[:16]
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC, iv=iv)
flag = b"THJCC{TEST_ME}"
ciphertext = iv + cipher.encrypt(pad(flag, 16))

print(f"E0: {E0.a_invariants()}")
print(f"Eab: {Eab.a_invariants()}")
print(f"P_pub: {P_pub.xy()}")
print(f"ciphertext: {ciphertext.hex()}")

# Output~
'''
E0: (0, 6, 0, 1, 0)
Eab: (0, 6, 0, 11067381*i + 1118198, 8021433*i + 1906048)
P_pub: (8959148*i + 2448181, 10026959*i + 706144)
ciphertext: 1aca81de78c79d95adc0b14f4dfb3c8121f900896c4ddd05fba6070f12f9a5ce94782503d5f8343ea8d237ea1eb13e76464a88cd4992fcad27e11af22b3fcd1a
'''