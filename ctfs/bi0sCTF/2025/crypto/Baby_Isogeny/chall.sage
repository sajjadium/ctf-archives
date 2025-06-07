#!/usr/bin/env sage
import os, sys, hashlib
from Crypto.Cipher import AES

e2, e3 = 216, 137
p = 2**e2 * 3**e3 - 1
F.<i> = GF(p**2, modulus=x^2+1)
E0 = EllipticCurve(F, [0,6,0,1,0])

def generate_torsion_basis(E, l, e, cofactor):
    while True:
        P = cofactor * E.random_point()
        if (l^(e-1)) * P != 0: 
            break
    while True:
        Q = cofactor * E.random_point()
        if (l^(e-1)) * Q != 0 and P.weil_pairing(Q, l^e) != 1:
            break
    return P, Q

P2, Q2 = generate_torsion_basis(E0, 2, e2, 3^e3)
P3, Q3 = generate_torsion_basis(E0, 3, e3, 2^e2)

def comp_iso(E, Ss, ℓ, e):
    φ,  E1 = None, E
    for k in range(e):
        R = [ℓ**(e-k-1) * S for S in Ss]
        ϕk = E1.isogeny(kernel=R)
        Ss = [ϕk(S) for S in Ss]
        E1 = ϕk.codomain()
        φ  = ϕk if φ is None else ϕk * φ
    return φ, E1

def j_ex(E, sk, pk, ℓ, e):
    φ, _ = comp_iso(E, [pk[0] + sk*pk[1]], ℓ, e)
    return φ.codomain().j_invariant()

def aes_cbc_encrypt(key, pt):
    iv = os.urandom(16)
    c  = AES.new(hashlib.sha256(key).digest()[:16], AES.MODE_CBC, iv)
    return iv, c.encrypt(pt)

def recv_K_elem(prompt):
    print(prompt)
    re = ZZ(input("  re: "))
    im = ZZ(input("  im: "))
    return F(re + i*im)

supersingular_cache = set()
def is_supersingular(Ei):
    a = Ei.a_invariants()
    if a in supersingular_cache:
        return True
    result = Ei.is_supersingular(proof=False)
    if result:
        supersingular_cache.add(a)
    return result

def recv():
    print("input your public key:")
    a1 = recv_K_elem("a1: ")
    a2 = recv_K_elem("a2: ")
    a3 = recv_K_elem("a3: ")
    a4 = recv_K_elem("a4: ")
    a6 = recv_K_elem("a6: ")
    Ei = EllipticCurve(F, [a1,a2,a3,a4,a6])
    assert(is_supersingular(Ei))
    Px = recv_K_elem("Px: ")
    Py = recv_K_elem("Py: ")
    P = Ei(Px, Py)
    Qx = recv_K_elem("Qx: ")
    Qy = recv_K_elem("Qy: ")
    Q = Ei(Qx, Qy)
    assert(P*(3^e3) == Ei(0) and P*(3^(e3-1)) != Ei(0))
    assert(Q*(3^e3) == Ei(0) and Q*(3^(e3-1)) != Ei(0))
    assert(P.weil_pairing(Q, 3^e3) == (P3.weil_pairing(Q3, 3^e3))^(2^e2))
    return (Ei, P, Q)

kA = randint(1,2**e2-1)
φA, EA = comp_iso(E0, [P2 + kA*Q2], 2, e2)
φAPB = φA(P3)
φAQB = φA(Q3)
φAPA = φA(P2) 
φAQA = φA(Q2)

j1 = j_ex(E0, kA, (P3,Q3), 3, e3)
flag1 = open('flag1.txt','rb').read().rjust(16,b'\x00')
iv1, ct1 = aes_cbc_encrypt(str(j1).encode(), flag1)

kB = randint(1, 3^e3 - 1)
φB, EB = comp_iso(E0, [P3 + kB*Q3], 3, e3)
φBPA = φB(P2)
φBQA = φB(Q2)

j2 = j_ex(E0, kB, (P2,Q2), 2, e2)
flag2 = open('flag2.txt','rb').read().rjust(16,b'\x00')
iv2, ct2 = aes_cbc_encrypt(str(j2).encode(), flag2)

print("\n=== public key ===")
print("PA:", P2.xy())
print("QA:", Q2.xy())
print("PB:", P3.xy())
print("QB:", Q3.xy())
print("EA invariants:", EA.a_invariants())
print("φAPB:", φAPB.xy())
print("φAQB:", φAQB.xy())
print("φAPA:", φAPA.xy())
print("φAQA:", φAQA.xy())
print("EB invariants:", EB.a_invariants())
print("φBPA:", φBPA.xy())
print("φBQA:", φBQA.xy())
print("IV1:", iv1.hex())
print("CT1:", ct1.hex())
print("IV2:", iv2.hex())
print("CT2:", ct2.hex())

print("\nNow you may submit your flag")
for _ in range(300):
    try:
        pk2 = recv()
        Ei, P, Q = pk2
        iv = bytes.fromhex(input("IV? ").strip())
        ct = bytes.fromhex(input("CT? ").strip())
        j  = j_ex(Ei, kB, (P,Q), 3, e3)
        key= hashlib.sha256(str(j).encode()).digest()[:16]
        pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
        print("Good!" if pt == flag1 else "Bad!")
    except:
        print("Error!") ; sys.exit(1)
