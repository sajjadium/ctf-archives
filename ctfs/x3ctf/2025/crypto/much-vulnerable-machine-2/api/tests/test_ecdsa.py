import pytest
from mvmcryption.crypto.ecdsa import ECDSA, decode_signature, encode_signature


@pytest.mark.parametrize("msg", [b"helo", b'{"get pwned": 1337}'])
@pytest.mark.parametrize("d", [1337, 895])
def test_ecdsa(msg: bytes, d: int):
    ecdsa = ECDSA(d)
    sig = ecdsa.sign(msg)

    assert ecdsa.verify(sig, msg)


@pytest.mark.parametrize("msg", [b"helo", b'{"get pwned": 1337}'])
@pytest.mark.parametrize("d", [1337, 895])
def test_ecdsa_signature_encoding_decoding(msg: bytes, d: int):
    ecdsa = ECDSA(d)
    sig = ecdsa.sign(msg)
    encoded_sig = encode_signature(sig)
    assert ecdsa.verify(decode_signature(encoded_sig.split(".")), msg)
