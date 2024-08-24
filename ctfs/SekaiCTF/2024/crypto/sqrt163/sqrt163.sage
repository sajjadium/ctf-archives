from ast import literal_eval
from hashlib import sha256
from Crypto.Cipher import AES

ells = [*primes(3, 128), 163]
p = 4 * prod(ells) - 1
F = GF(p)

def csidh(A, priv):
    E = EllipticCurve(F, [0, A, 0, 1, 0])
    for sgn in [1, -1]:
        for e, ell in zip(priv, ells):
            for i in range(sgn * e):
                while not (P := (p + 1) // ell * E.random_element()):
                    pass
                E = E.isogeny_codomain(P)
        E = E.quadratic_twist()
    return E.montgomery_model().a2()

# This is the private key for the 163-isogeny, given by [0, 0, ..., 0, 1]
priv_163 = [int(ell == 163) for ell in ells]
pub_163 = csidh(0, priv_163)

# This is the private key for the sqrt(163)-isogeny, such that if you square it you get the 163-isogeny
priv_rt163 = literal_eval(input("Enter private key: "))
pub_rt163 = csidh(0, priv_rt163)

assert csidh(pub_rt163, priv_rt163) == pub_163, "Your private key does not define a sqrt(163)-isogeny!"

ct = 'efee2dfd387fe42a983089c517d4e479c98242da5687c62548ca12a06096962e6271ef268600406fde4f0ee50c844f42aac23cd9cf0f07e4822c4045daf917d4'
print(AES.new(sha256(str(pub_rt163).encode()).digest(), AES.MODE_ECB).decrypt(bytes.fromhex(ct)).decode())