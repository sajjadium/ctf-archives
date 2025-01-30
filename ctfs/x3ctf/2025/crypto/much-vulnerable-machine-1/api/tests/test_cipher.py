from random import getrandbits

import pytest
from Crypto.Util.number import long_to_bytes
from mvmcryption.crypto.cipher import SCBCCipher


@pytest.mark.parametrize("msg", [b"helo", b'{"get pwned": 1337}'])
@pytest.mark.parametrize("d", [1337, 895])
def test_scbccipher(msg: bytes, d: int):
    key = long_to_bytes(d, 16)
    ciph = SCBCCipher(key)

    iv = long_to_bytes(getrandbits(128), 16)
    ct = ciph.encrypt(msg, iv)

    assert ct
    assert msg == ciph.decrypt(ct, iv)
