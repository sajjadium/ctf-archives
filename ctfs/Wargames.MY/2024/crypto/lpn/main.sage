from hashlib import sha256
import os
import secrets
import signal

FLAG = 'wgmy{fake_flag}'

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 240
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

F.<z> = GF(2^128)
n = 20; m = 100

seed = os.urandom(16)
set_random_seed(int.from_bytes(seed, 'big'))
A = [[F.random_element() for _ in range(m)] for _ in range(n)]
A = Matrix(F, A)

set_random_seed(int.from_bytes(os.urandom(16), 'big'))
e_elem_1 = F.random_element()
e_elem_2 = F.random_element()
assert e_elem_1 != e_elem_2

s = vector(F, [F.random_element() for _ in range(n)])
e = vector(F, [e_elem_1 if secrets.randbits(1) else e_elem_2 for _ in range(m)])

b = s * A + e

print(f'{seed.hex() = }')
print(f'{list(b) = }')

s_ = input('hash(s): ')
if s_ == str(sha256(str(list(s)).encode()).hexdigest()):
    print(FLAG)
else:
    print("WRONG")