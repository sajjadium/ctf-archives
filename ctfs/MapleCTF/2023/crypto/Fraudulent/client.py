from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from random import randint
from hashlib import sha256

p = 81561774084914804116542793383590610809004606518687125749737444881352531178029
g = 2
q = p - 1
x = 1               # Your private key
X = pow(g, x, p)

def hash(values):
    h = sha256()
    for v in values:
        h.update(long_to_bytes(v))
    return bytes_to_long(h.digest())

def create_proof(encrypted_vote, r):
    R, S = encrypted_vote

    c_0 = randint(0, q - 1)
    f_0 = randint(0, q - 1)
    a_1 = randint(0, q - 1)

    A_0 = pow(g, f_0, p) * pow(R, -c_0, p) % p
    B_0 = pow(X, f_0, p) * pow(S, -c_0, p) % p

    A_1 = pow(g, a_1, p)
    B_1 = pow(X, a_1, p)

    print([A_0, B_0, A_1, B_1])
    c = hash([A_0, B_0, A_1, B_1])
    
    c_1 = c - c_0
    f_1 = a_1 + c_1 * r
    return (c_0, c_1, f_0, f_1)

def encrypt(m):
    # Encrypt message
    y = randint(0, q - 1)
    s = pow(X, y, p)
    c_1 = pow(g, y, p)
    c_2 = pow(g, m, p) * s % p
    R, S = c_1, c_2

    # Generate proof that encrypted message is either 0 or 1
    if m == 0:
        c_1 = randint(0, q - 1)
        f_1 = randint(0, q - 1)
        a_0 = randint(0, q - 1)

        S_p = S * pow(g, -1, p) % p
        A_1 = pow(g, f_1, p) * pow(R, -c_1, p) % p
        B_1 = pow(X, f_1, p) * pow(S_p, -c_1, p) % p

        A_0 = pow(g, a_0, p)
        B_0 = pow(X, a_0, p)

        c = hash([A_0, B_0, A_1, B_1])
        
        c_0 = c - c_1
        f_0 = a_0 + c_0 * y
        return (R, S), (c_0, c_1, f_0, f_1)
    elif m == 1:
        c_0 = randint(0, q - 1)
        f_0 = randint(0, q - 1)
        a_1 = randint(0, q - 1)

        A_0 = pow(g, f_0, p) * pow(R, -c_0, p) % p
        B_0 = pow(X, f_0, p) * pow(S, -c_0, p) % p

        A_1 = pow(g, a_1, p)
        B_1 = pow(X, a_1, p)

        c = hash([A_0, B_0, A_1, B_1])
        
        c_1 = c - c_0
        f_1 = a_1 + c_1 * y
        return (R, S), (c_0, c_1, f_0, f_1)

    else:
        raise Exception(f"Cannot encrypt message {m}!")


def verify_vote(encrypted_vote, proof):
    R, S = encrypted_vote
    c_0, c_1, f_0, f_1 = proof

    values = [
        pow(g, f_0, p) * pow(R, -c_0, p) % p,
        pow(X, f_0, p) * pow(S, -c_0, p) % p,
        pow(g, f_1, p) * pow(R, -c_1, p) % p,
        pow(X, f_1, p) * pow(S, -c_1, p) * pow(g, c_1, p) % p,
    ]

    return c_0 + c_1 == hash(values)


encrypted_vote, proof = encrypt(1)
print("(R, S):", encrypted_vote)
print("(C0, C1, F0, F1):", proof)
assert verify_vote(encrypted_vote, proof)