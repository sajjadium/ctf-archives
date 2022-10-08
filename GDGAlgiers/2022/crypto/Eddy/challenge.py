from pure25519.basic import (bytes_to_clamped_scalar,scalar_to_bytes,
                             bytes_to_scalar,
                             bytes_to_element, Base)
import hashlib, binascii
import os


def H(m):
    return hashlib.sha512(m).digest()


def publickey(seed):
    # turn first half of SHA512(seed) into scalar, then into point
    assert len(seed) == 32
    a = bytes_to_clamped_scalar(H(seed)[:32])
    A = Base.scalarmult(a)
    return A.to_bytes()


def Hint(m):
    h = H(m)
    return int(binascii.hexlify(h[::-1]), 16)


def signature(m, sk, pk):
    assert len(sk) == 32  # seed
    assert len(pk) == 32
    h = H(sk[:32])
    a_bytes, inter = h[:32], h[32:]
    a = bytes_to_clamped_scalar(a_bytes)
    r = Hint(inter + m)
    R = Base.scalarmult(r)
    R_bytes = R.to_bytes()
    S = r + Hint(R_bytes + pk + m) * a
    e = Hint(R_bytes + pk + m)
    return R_bytes, S, e


def checkvalid(s, m, pk):
    if len(s) != 64: raise Exception("signature length is wrong")
    if len(pk) != 32: raise Exception("public-key length is wrong")
    R = bytes_to_element(s[:32])
    A = bytes_to_element(pk)
    S = bytes_to_scalar(s[32:])
    h = Hint(s[:32] + pk + m)
    v1 = Base.scalarmult(S)
    v2 = R.add(A.scalarmult(h))
    return v1 == v2


def create_signing_key():
    seed = os.urandom(32)
    return seed


def create_verifying_key(signing_key):
    return publickey(signing_key)
