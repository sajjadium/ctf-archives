import os
import random
import numpy as np
import signal

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 180
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

FLAG = 'wgmy{fake_flag}'

def change_support(support):
    while (t := random.randint(0, n - 1)) in support: pass
    support[random.randint(0, k - 1)] = t
    return support

n = 500; p = 3691; k = 10; m = 20 * n

seed = os.urandom(16)
random.seed(seed)

A = np.zeros((n, m), dtype=int)
support = random.sample(range(n), k)

columns = list(range(m))
random.shuffle(columns)

for i in columns:
    if (random.randint(0, 2) == 0):
        support = change_support(support)
    A[support, i] = [random.randint(0, p - 1) for _ in range(k)]

secure_random = random.SystemRandom()
s = np.array([secure_random.randint(0, p - 1) for _ in range(n)])
e = np.round(np.random.normal(0, 1, size=m)).astype(int)

b = (s @ A + e) % p
print(f'{seed.hex() = }')
print(f'{b.tolist() = }')

s_ = input('s: ')
if s_ == str(s.tolist()):
    print(FLAG)
else:
    print("WRONG")
