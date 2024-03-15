
from Crypto.Util.number import getStrongPrime
from Crypto.Random.random import randint

## Implementation of Pedersen Commitment Scheme
## Computationally binding, information theoreticly hiding

# Generate public key for Pedersen Commitments
def gen():
    q = getStrongPrime(1024)
    
    g = randint(1,q-1)
    s = randint(1,q-1)
    h = pow(g,s,q)

    return q,g,h

# Create Pedersen Commitment to message x
def commit(pk, m):
    q, g, h = pk
    r = randint(1,q-1)

    comm = pow(g,m,q) * pow(h,r,q)
    comm %= q

    return comm,r

# Verify Pedersen Commitment to message x, with randomness r
def verify(param, c, r, x):
    q, g, h = param
    if not (x > 1 and x < q):
        return False
    return c == (pow(g,x,q) * pow(h,r,q)) % q