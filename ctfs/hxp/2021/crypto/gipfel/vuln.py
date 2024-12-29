#!/usr/bin/env python3
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import signal, random
random = random.SystemRandom()

q = 0x3a05ce0b044dade60c9a52fb6a3035fc9117b307ca21ae1b6577fef7acd651c1f1c9c06a644fd82955694af6cd4e88f540010f2e8fdf037c769135dbe29bf16a154b62e614bb441f318a82ccd1e493ffa565e5ffd5a708251a50d145f3159a5

def enc(a):
    f = {str: str.encode, int: int.__str__}.get(type(a))
    return enc(f(a)) if f else a

def H(*args):
    data = b'\0'.join(map(enc, args))
    return SHA256.new(data).digest()

def F(h, x):
    return pow(h, x, q)

################################################################

password = random.randrange(10**6)

def go():
    g = int(H(password).hex(), 16)

    privA = 40*random.randrange(2**999)
    pubA = F(g, privA)
    print(f'{pubA = :#x}')

    pubB = int(input(),0)
    if not 1 < pubB < q:
        exit('nope')

    shared = F(pubB, privA)

    verA = F(g, shared**3)
    print(f'{verA = :#x}')

    verB = int(input(),0)
    if verB == F(g, shared**5):
        key = H(password, shared)
        flag = open('flag.txt').read().strip()
        aes = AES.new(key, AES.MODE_CTR, nonce=b'')
        print(f'flag:', aes.encrypt(flag.encode()).hex())
    else:
        print(f'nope! {shared:#x}')

# three shots, three opportunities
# to seize everything you ever wanted
# would you capture? or just let it slip?
signal.alarm(2021)
go()
go()
go()

