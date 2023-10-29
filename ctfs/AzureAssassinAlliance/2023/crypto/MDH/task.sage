from hashlib import sha256
from secret import flag

r = 128
c = 96
p = 308955606868885551120230861462612873078105583047156930179459717798715109629
Fp = GF(p)

def gen():
    a1 = random_matrix(Fp, r, c)
    a2 = random_matrix(Fp, r, c)
    A = a1 * a2.T
    return (a1, a2), A

sk_alice, pk_alice = gen()
sk_bob, pk_bob = gen()
shared = (sk_alice[0].T * pk_bob * sk_alice[1]).trace()
ct = int(sha256(str(int(shared)).encode()).hexdigest(), 16) ^^ int.from_bytes(flag, 'big')

with open('output.txt', 'wb') as f:
    f.write(str(ct).encode() + b'\n')
    f.write(str(list(pk_alice)).encode() + b'\n')
    f.write(str(list(pk_bob)).encode() + b'\n')
