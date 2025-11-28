import numpy as np
import json

try:
    from flag import flag
except: 
    flag = "redacted_this_is_just_so_that_it_works_and_you_can_test_locally."

m_b = np.array([int(c) for char in flag for c in format(ord(char), '08b')])

# Parameters
q = 3329
n = 512
k = 4
f = np.array([1] + [0]*(n-1) + [1])

assert len(m_b)==n

# ---------- Helper functions ----------
def _small_noise(n, weight=2):
    coeffs = np.zeros(n, dtype=int)
    idx = np.random.choice(n, size=weight, replace=False)
    signs = np.random.choice([-1, 1], size=weight)
    coeffs[idx] = signs
    return coeffs

def _vec_poly_mul(v0, v1):
    def _poly_mul(a, b):
        res = np.convolve(a, b)
        for i in range(n, len(res)):
            res[i - n] = (res[i - n] - res[i]) % q 
        return res[:n] % q
    return sum((_poly_mul(a, b) for a, b in zip(v0, v1))) % q

def encrypt(A, t, m_b, r, e_1, e_2):
    u = np.array([(mat + err) % q for mat, err in 
         zip([_vec_poly_mul(row, r) for row in A.T], e_1)
         ])
    tr = _vec_poly_mul(t, r)
    m = (m_b * ((q + 1)//2)) % q
    v = (tr + e_2 + m) % q
    return u, v

# ---------- Key generation ----------
A_1 = np.array([np.array([np.random.randint(0, q, n) for _ in range(k)]) for _ in range(k)])
A_2 = np.array([np.array([np.random.randint(0, q, n) for _ in range(k)]) for _ in range(k)])
s_1 = np.array([_small_noise(n, n*2//3) for _ in range(k)])
s_2 = np.array([_small_noise(n, n*2//3) for _ in range(k)])
e = np.array([_small_noise(n) for _ in range(k)])
t_1 = np.array([(_vec_poly_mul(row, s_1) + err) % q for row, err in zip(A_1, e)])
t_2 = np.array([(_vec_poly_mul(row, s_2) + err) % q for row, err in zip(A_2, e)])

# ---------- Encryption ----------
r = [_small_noise(n) for _ in range(k)]
e_1 = [_small_noise(n) for _ in range(k)]
e_2 = _small_noise(n)

u_1, v_1 = encrypt(A_1, t_1, m_b, r, e_1, e_2)
u_2, v_2 = encrypt(A_2, t_2, m_b, r, e_1, e_2)

# ---------- Giving keys to user ---------------

keys = {
    "A_1" : A_1.tolist(),
    "t_1" : t_1.tolist(),
    "A_2" : A_2.tolist(),
    "t_2" : t_2.tolist(),
    "u_1" : u_1.tolist(),
    "u_2" : u_2.tolist(),
    "v_1" : v_1.tolist(),
    "v_2" : v_2.tolist() 
}

with open("keys.json", "w") as f:
    f.write(json.dumps(keys))

