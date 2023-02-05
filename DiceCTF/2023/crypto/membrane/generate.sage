import numpy as np

# dimension
n = 512
# number of public key samples
m = n + 100
# plaintext modulus
p = 257
# ciphertext modulus
q = 1048583

V = VectorSpace(GF(q), n)
S = V.random_element()

def encrypt(m):
    A = V.random_element()
    e = randint(-10, 10)
    b = A * S + m + p * e
    return A, b

def decrypt(A, b):
    A = V(A)
    m = ZZ(b - A * S)
    if m > q//2:
        m -= q
    m = ZZ(m % p)
    return m

def public_key_encrypt(public_key_samples_A, public_key_samples_b, msg):
    c = vector(ZZ, [randint(-1,1) for i in range(m)])
    e = randint(-10, 10)

    A = c * public_key_samples_A
    b = c * public_key_samples_b + msg + p * e
    
    return A,b


def keygen():
    public_key_samples_A = []
    public_key_samples_b = []
    for i in range(m):
        A, b = encrypt(0)
        public_key_samples_A.append(A)
        public_key_samples_b.append(b)
        
    public_key_samples_A = Matrix(GF(q), public_key_samples_A)
    public_key_samples_b = vector(GF(q), public_key_samples_b)

    return public_key_samples_A, public_key_samples_b


with open("flag.txt", "rb") as f:
    flag = f.read()


pk_A, pk_b = keygen()

encrypt_A, encrypt_b = [], []
for msg in flag:
    A, b = public_key_encrypt(pk_A, pk_b, msg)
    encrypt_A.append(A)
    encrypt_b.append(b)


pk_A = np.array(pk_A, dtype=np.int64)
pk_b = np.array(pk_b, dtype=np.int64)
encrypt_A = np.array(encrypt_A, dtype=np.int64)
encrypt_b = np.array(encrypt_b, dtype=np.int64)
np.savez_compressed("data.npz", pk_A=pk_A, pk_b=pk_b, encrypt_A=encrypt_A, encrypt_b=encrypt_b)
