from string import ascii_letters
from sympy import sqrt
import random
import signal
import os
FLAG = os.environ.get('FLAG', 'n1ctf{XXXXFAKE_FLAGXXXX}')    
    
def banner():
    print("""
░░░░░░░ ░░░░░░  ░░ ░░░░░░░  ░░░░░░  
▒▒           ▒▒ ▒▒ ▒▒      ▒▒    ▒▒ 
▒▒▒▒▒    ▒▒▒▒▒  ▒▒ ▒▒▒▒▒▒▒ ▒▒    ▒▒ 
▓▓      ▓▓      ▓▓      ▓▓ ▓▓    ▓▓ 
███████ ███████ ██ ███████  ██████  
    """)

def curve_init():
    p = random_prime(2^256)
    F.<i> = GF(p^2, modulus = x**2 + 1)
    R.<t> = PolynomialRing(GF(p))
    guess = ''.join(random.choices(ascii_letters, k=20))
    RR = RealField(256)
    num = RR(int(guess.encode().hex(),16))
    j = F(str(sqrt(num)).split('.')[1])
    E = EllipticCurve(j=j)
    P = E(0).division_points(3)
    P.remove(E(0))
    phi = E.isogeny(random.choice(P))
    E2 = phi.codomain()
    j2 = E2.j_invariant()
    assert list(R(j2))[1] != 0
    return E2, p, guess

def leak(E, p):
    F = Zmod(p^2)
    R.<t> = PolynomialRing(GF(p))
    r = random.getrandbits(20)
    x = F(input("your magic number?\n$ "))^r - 1
    j_ = E.j_invariant()^x
    print(list(R(j_))[0])

def main():
    signal.alarm(120)
    banner()
    para = None
    print("Curve Initialization...")
    while not para:
        try:
            para = curve_init()
        except:
            continue
    E, p, guess = para
    print(f"einfo: {E.base_ring()}")
    leak(E, p)
    if input("guess > ").strip('\n') == guess:
        print(f"Congratz, your flag: {FLAG}")
    else:
        print("Game over!")
        

if __name__ == "__main__":
    try:
        main()
    except:
        print("error!")