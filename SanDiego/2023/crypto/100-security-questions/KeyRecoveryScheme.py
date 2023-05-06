import hashlib
from fractions import Fraction
from Crypto.Random.random import randrange
from Crypto.Protocol.KDF import scrypt
from math import gcd

# this scheme is taken from a paper by Ellison, Hall, Milbert and Schneier
# titled "Protecting secret keys with personal entropy"

KEY_LENGTH = 16
p = 258641170704651026037450395747679449699 # picked as a safe prime, i.e. (p - 1) / 2 is also prime

class Cipher(): # It takes in an answer (encoded as (question #, answer)) as a key, and maps Z_n -> Z_n on a fixed key.
    def __init__(self, share, n): # k is the share that is "derived" into an appropriate Pohlig-Hellman key
        self.n = n # n should be prime, this function does not perform checks though
        hasher = hashlib.sha256()
        hasher.update(str(share).encode())
        self.e = int(hasher.hexdigest(), 16) % (n - 1) # we make e fall into Z_m where m is the order of the group
        while gcd(self.e, n - 1) != 1:
            self.e += 1
        self.d = pow(self.e, -1, n - 1)
    
    def encrypt(self, M):
        return pow(M, self.e, self.n)

    def decrypt(self, C):
        return pow(C, self.d, self.n)


def eval_polynomial(x, poly_coeff, n): # evaluate a polynomial on x over the field Z_n
    result = 0
    for i in range(len(poly_coeff)):
        term = (poly_coeff[i] * pow(x, i, n)) % n
        result = (result + term) % n
    return result

def std_lagrange_coeff(i, x_lst, n): # get the ith standard Lagrange coefficient, under modulus n, where n is a prime (so order of group is (n - 1))
    result = Fraction(1,1)
    for j in range(len(x_lst)):
        if (j == i): continue
        result *= x_lst[j]
        result *= pow(x_lst[j] - x_lst[i], -1, n)
    return result

def h(j):
    # referred to following URL to select parameters:
    # https://stackoverflow.com/questions/11126315/what-are-optimal-scrypt-work-factors
    return scrypt(str(j), "", KEY_LENGTH, 1048576, 8, 1)

class KeyRecoveryScheme():
    def __init__(self, k, n):
        self.k = k
        self.n = n
    
    # answers are a list of tuples in the form (question #, answer string (NOT bytestring)). Note that the question # is 1-indexed.
    def Lock(self, answers): # generate random 128-bit key to be used for AES, and also its locked counterpart.
        assert(len(answers) == self.n)
        poly_coeff = [randrange(p) for _ in range(self.k)] # generate random (k - 1) degree polynomial with coefficients in Z_p
        s_i = [] # this is our lock, which contains all encrypted y-values for x = 1, 2, ..., n
        for (j, a) in answers: # answers in form (1, "answer1"), (2, "answer2"), ...
            y_val = eval_polynomial(j, poly_coeff, p) # evaluate polynomial on x = 1, 2, ..., n
            s_i.append(Cipher((j, a), p).encrypt(y_val))
        key = h(poly_coeff[0])
        lock = ",".join(map(lambda x: str(x), s_i)).encode()
        return (key, lock)

    def Unlock(self, answers, lock):
        assert(len(answers) >= self.k)
        enc_y_lst = [int(x) for x in lock.decode().split(",")]
        coordinates = []
        for (j, t) in answers:
            # note that the Cipher takes in the entire (question #, answer) tuple as the key, not just the answer.
            coordinates.append((j, Cipher((j, t), p).decrypt(enc_y_lst[j - 1]))) # decrypt the y-values in the lock
        assert(len(coordinates) == len(answers))
        poly_0 = 0 # the evaluation of the polynomial at 0 (what we want to find)
        # interpolate the polynomial to find its evaluation at x = 0, using Lagrange interpolation
        x_lst = list(map(lambda x: x[0], coordinates))
        for j in range(len(coordinates)):
            lagrange_basis = (coordinates[j][1] * std_lagrange_coeff(j, x_lst, p)) % p
            poly_0 = (poly_0 + lagrange_basis) % p
        key = h(poly_0)
        return key