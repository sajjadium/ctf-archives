import random
from utilities import *
import os
import signal

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("snakeCTF{"))
assert(FLAG.endswith("}"))

class PolynomialGenerator:
    def gen_from_uniform_distribution(B, modulo, N_values, ring):
        coefficients = [randint(0, B) % modulo for i in range(N_values)]
        return coefficients_to_poly(ring, coefficients)

    def zero_polynomial(N_values, ring):
        coefficients = [0 for i in range(N_values)]
        return coefficients_to_poly(ring, coefficients)


def coefficients_to_poly(ring, coefficients):
    p = 0
    for i in coefficients:
        p = p*x+i

    return ring(p)


class Cipher:
    N = None
    PK = None
    SK = None

    def __init__(self, N, p, irreducible_polynomial):
        self.N = N
        self.p = p
        
        # self.q, k = generate_NTTPrime(2*N, 60) we will not use NTT

        Z = Zmod(self.p)
        S = PolynomialRing(Z,'x')
        R = S.quotient(irreducible_polynomial, 'x')

        self.ring = R
        self.coefficient_modulo = Z

        
        
    def key_gen(self): # returns a secret key from R2
        list_of_sk = [ PolynomialGenerator.gen_from_uniform_distribution(1, self.p, self.N, self.ring) for _ in range(2)]
        list_of_public_poly = [ PolynomialGenerator.gen_from_uniform_distribution(self.p, self.p, self.N, self.ring) for _ in range(4) ]
        list_of_e = [ PolynomialGenerator.gen_from_uniform_distribution(1, self.p, self.N, self.ring) for _ in range(2)] # error with small coefficients

        self.A = Matrix(self.ring, 2, 2, list_of_public_poly)
        self.SK = Matrix(self.ring, 2, 1, list_of_sk)
        self.e = Matrix(self.ring, 2, 1, list_of_e)
        
        self.b = self.A*self.SK + self.e
        self.PK = (self.A, self.b)
        return self.PK

   
    def encrypt(self, message: int):
        # message is an integer
        M_1 = binary_encode_message(message,self.N)
        M = coefficients_to_poly(self.ring, M_1)

        r = [ PolynomialGenerator.gen_from_uniform_distribution(1, self.p, self.N, self.ring) for _ in range(2)]
        e1 = [ PolynomialGenerator.gen_from_uniform_distribution(1, self.p, self.N, self.ring) for _ in range(2)]# error with small coefficients
        e2 = PolynomialGenerator.gen_from_uniform_distribution(1, self.p, self.N, self.ring) # error with small coefficients
        
        r = Matrix(self.ring,2, 1, r )
        e1 = Matrix(self.ring, 2, 1, e1)
        e2 = Matrix(self.ring, [e2])
        
        A, b = self.PK

        delta = math.ceil( self.p / 2 )
        m = M*delta
        m = Matrix(self.ring, [m])
        u =  A.transpose()*r + e1 
        
        v = b.transpose()*r + e2 + m
        C = (u,v)
        return C



def encrypt_string(cipher, message):
    for c in message:
        u, v = cipher.encrypt(int(ord(c)))

        print("(", end=" ")
        print(list(u), end=" ")
        print(",", end=" ")
        print(list(v), end=" ")
        print(")")
     

def main():
    p = 65537  
    N = 8 # the degree of the polynomials will be N-1

    print("Welcome to this new strong encrytion system.\nThese cryptosystem was initialized with the following parameters:\n")
    print(f'N = {N}')
    print(f'Prime p = {p}')
    
    # cipher initialization
    irreducible_polynomial = x^8+x^7+x^6+x^5+1
    cipher = Cipher(N, p, irreducible_polynomial)
    PK = cipher.key_gen()

    print()
    print("Here is my Public Key (A, b):\n")
    print()
    print(f'A = {list(PK[0])}')
    print()
    print(f'b = {list(PK[1])}')
    
    print("\nWe are now encrypting your flag a character per time.....", flush=True)
    encrypt_string(cipher, FLAG)
    



if __name__ == "__main__":
    main()

