from Crypto.Util.number import getPrime
from hashlib import sha512
import random
import signal

FLAG = 'wgmy{fake_flag}'

def _handle_timeout(signum, frame):
    raise TimeoutError('function timeout')

timeout = 60
signal.signal(signal.SIGALRM, _handle_timeout)
signal.alarm(timeout)

def xor(a, b):
    return bytes(x^^y for x, y in zip(a, b))

secure_random = random.SystemRandom()
p = getPrime(64)
F.<z> = GF(p^4)

a = secure_random.randint(0, p-1); b = secure_random.randint(0, p-1)
E = EllipticCurve(F, [a, b])
P = E.gens()[0]

print(f'{p = }'); print(f'{F.modulus() = }')
print(f'{E.j_invariant() = }'); print(f'{P.xy() = }')

Qx = F(list(map(int, input('Qx:').split(' '))))
Q = E.lift_x(Qx)

k = int(input('k:'))
assert 1 <= k <= E.order() - 1

for _ in range(10):
    Tx, Ty = Q.x()^p, Q.y()^p
    Hx, Hy = (k * Q).xy()
    Q = E(Tx, Ty) + E(Hx, Hy)
Q = Q + p * E.lift_x(Qx)

if (Q == P):
    print("FLAG", xor(FLAG.encode(), sha512((str(a) + str(b)).encode()).digest()).hex())
else:
    print("WRONG")