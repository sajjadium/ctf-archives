import numpy as np
import json

# message
try:
    from flag import flag
except:
    flag = "redacted_this_is_just_so_that_it_works_and_you_can_test_locally."

m_process = [int(c) for char in flag for c in format(ord(char), '08b')]

# Parameters
q = 251
n = 16
k = 2
f = np.array([1] + [0]*(n-1) + [1])

m_b = np.array([m_process[i:i+16] for i in range(0, len(m_process), n)])

assert len(m_b[0])%n == 0
batch_size = m_b.shape[0]

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

def encrypt(A, t, m_b_batch, r_batch, e_1_batch, e_2_batch):
    A_T = list(map(list, zip(*A)))    
    u_list = []
    v_list = []
    for b in range(batch_size):
        r = r_batch[b]
        e_1 = e_1_batch[b]
        e_2 = e_2_batch[b]
        m_b = m_b_batch[b]        
        u = np.array([(mat + err) % q for mat, err in 
             zip([_vec_poly_mul(row, r) for row in A_T], e_1)
             ])
        tr = _vec_poly_mul(t, r)

        m = (m_b * ((q + 1)//2)) % q
        
        v = (tr + e_2 + m) % q
        
        u_list.append(u)
        v_list.append(v)
        
    return np.array(u_list), np.array(v_list)

# ---------- Key generation ----------
A = np.array([np.array([np.random.randint(0, q, n) for _ in range(k)]) for _ in range(k)])
s = np.array([_small_noise(n, n//2) for _ in range(k)])
e = np.array([_small_noise(n) for _ in range(k)])
t = np.array([(_vec_poly_mul(row, s) + err) % q for row, err in zip(A, e)])

# ---------- Encryption ----------
r_batch = np.array([[_small_noise(n) for _ in range(k)] for _ in range(batch_size)])
e_1_batch = np.array([[_small_noise(n) for _ in range(k)] for _ in range(batch_size)])
e_2_batch = np.array([_small_noise(n) for _ in range(batch_size)])

u, v = encrypt(A, t, m_b, r_batch, e_1_batch, e_2_batch)

# ---------- Saving key ---------------
keys = {
    "A": A.tolist(),
    "t": t.tolist(),
    "u": u.tolist(),
    "v": v.tolist()
}

with open("keys.json", "w") as f:
    f.write(json.dumps(keys))
