from sage.all import *

FLAG = b"kalmar{???}"

#Formulae from https://www.hyperelliptic.org/EFD/g1p/auto-montgom-xz.html
#dbl-1987-m-3
def double(a24, P):
    X1, Z1 = P

    A = X1+Z1
    AA = A*A
    B = X1-Z1
    BB = B*B
    C = AA-BB
    X3 = AA*BB
    Z3 = C*(BB+a24*C)

    return (X3, Z3)

#dadd-1987-m-3
def diff_add(P, Q, PmQ):
    X2, Z2 = P
    X3, Z3 = Q
    X1, Z1 = PmQ

    A = X2+Z2
    B = X2-Z2
    C = X3+Z3
    D = X3-Z3
    DA = D*A
    CB = C*B
    X5 = Z1*(DA+CB)**2
    Z5 = X1*(DA-CB)**2
    return (X5, Z5)

def ladder(a24, P, n):
    n = abs(n)
    P1, P2 = (1, 0), P
    if n == 0:
        return P1, P2
    for bit in bin(n)[2:]:
        Q = diff_add(P2, P1, P)
        if bit == "1":
            P2 = double(a24, P2)
            P1 = Q
        else:
            P1 = double(a24, P1)
            P2 = Q
    return P1

def keygen(A, G, ord_G):
    s = randint(1, ord_G)
    a24 = (A + 2)/4
    P = ladder(a24, G, s)
    return s, P

def derive_secret(A, Pub, sk):
    a24 = (A + 2)/4
    R = ladder(a24, Pub, sk)
    return int(R[0]/R[1])


if __name__=="__main__":
    p = 340824640496360275329125187555879171429601544029719477817787
    F = GF(p)
    A = F(285261811835788437932082156343256480312664037202203048186662)
    ord_G = 42603080062045034416140648444405950943345472415479119301079

    G = (F(2024), F(1))

    s_A, p_A = keygen(A, G, ord_G)
    print(f"Alice sending Bob...\n{p_A}")

    s_B, p_B = keygen(A, G, ord_G)
    print(f"Bob sending Alice...\n{p_B}")

    ss_A = derive_secret(A, p_B, s_A)
    ss_B = derive_secret(A, p_A, s_B)

    assert ss_A == ss_B

    import hashlib
    import os
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad

    def encrypt_flag(shared_secret: int):
        sha1 = hashlib.sha1()
        sha1.update(str(shared_secret).encode('ascii'))
        key = sha1.digest()[:16]
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(FLAG, 16))
        return iv.hex(), ciphertext.hex()

    print(encrypt_flag(ss_A))
