from Crypto.Cipher import AES
from Crypto.Util.number import getPrime, getRandomRange
from Crypto.Util.Padding import pad
import hashlib, itertools

from flag import FLAG

def normalize(fac):
    n = 1
    for p, e in fac:
        n *= p**e
    return n

def gen():
    private = []
    for _ in range(5):
        p = getPrime(512)
        e = getRandomRange(1, 4)
        private.append((p, e))
    return private, normalize(private)

def divs(fac, pre=None):
    if pre is None:
        pre = []
    if not fac:
        yield pre
    else:
        p, e = fac[0]
        for i in range(0, e + 1):
            yield from divs(fac[1:], pre + [(p, i)])

def div(a, b):
    b = dict(b)
    res = []
    for p, e in a:
        assert e >= b[p]
        res.append((p, e - b[p]))
    return res

def phi(fac):
    res = 1
    for p, e in fac:
        if not e: continue
        res *= (p**(e - 1)) * (p - 1)
    return res

def deriv(priv):
    res = 0
    for d1 in divs(priv):
        for d2 in divs(d1):
            res += normalize(d2) * phi(d2) * phi(div(d1, d2))
    return res

priv, pub = gen()
key = deriv(priv)
cipher = AES.new(hashlib.sha256(str(key).encode("utf-8")).digest(), AES.MODE_CBC, iv=b"\0" * 16)
ciphertext = cipher.encrypt(pad(FLAG.encode("utf-8"), 16))

print(f"pub: {hex(pub)}")
print(f"ciphertext: {ciphertext.hex()}")

###
# This printed:
#
# pub: 0x281ab467e16cdedb97a298249bdd334f0cc7d54177ed0946c04ec26da111c1fd7afa78fca045f81d89fe541f1d869b8edd4209c898a529737b9380ce9b47133ed9e097bcf050178c4a1ff92f35410ee589cc62617b63632f6c7aa506bdc50a79624246a63e4139a04a51f666cc53e21b7d4b12da7757feb367d47110af9bc707d92c9be2f2e4a51ea219cd9aacc76950f992ced96bab65ba654ded42af5fc4fec5330ebc29f377e733f1829b72f91e270c43e407d649d5cc1d38be9a0020cfe5cc537c131887b5a07a214eae2f0d9e684897590a637bd800fed6a61f6c034fe3a69d516d10a1e63aee3f71e067497d0d7ac1ec771cfae3ce89d82d69cd280622730e58b0427d193a5404f21f962e711d31c9a224e187031cf0e4bcdb341b65e999157fb55c7aae0cffed74b832a79259c18bf7b2db57e500d36376767973ee350af4fc004a7f4dcd325724a6994ca63687d3cfb688deb20e4175a67969ed7d245c207257eab7a71cc298532e72e73e446102e59a1a36de09c386445df171797e0d2db39f4fc1fba793d78ea92c6801b79eaef2ebaad54bd2a8106471adc60be708b9b0f4e824c25c414755ff56dace29c067e29c11a8adcc5f367e1c7d10310116eab8d99ddb2ae524f56bf9436f59e581c6e22b4a80d2520893c57aaafa0e6349347991f26b25b594bd47c5c0a69ed32c3fd0961f54586f3d91bf14d96d93d3f97c7a504ba8e3fe9e08316fe9f3d78500337a180120b5b375980ef19f57ff678a07b582ea3a113e2a0b14683ff3983153a2203cffd39fc7673281f72db700d
# ciphertext: d2463ccc52075674effbad1b1ea5ae9a9c8106f141cff8fdec9b118ddddcfb3a1f036ed5f3bf0440c95828ebf1c584e4
###
