from random import getrandbits, seed

import pytest
from Crypto.Util.number import long_to_bytes
from mvmcryption.crypto.cipher import XSCBCCipher
from mvmcryption.crypto.rsa import RSA


@pytest.mark.parametrize("msg", [b"helo", b'{"get pwned": 1337}'])
@pytest.mark.parametrize("d", [1337, 895])
def test_xscbccipher(msg: bytes, d: int):
    key = long_to_bytes(d, 16)
    rsa = RSA()
    ciph = XSCBCCipher(key, rsa)

    seed(69)
    iv = long_to_bytes(getrandbits(128), 16)
    seed(69)
    ct, sig = ciph.encrypt(msg)

    assert ct
    assert sig

    assert msg == ciph.decrypt(ct, sig, iv)
