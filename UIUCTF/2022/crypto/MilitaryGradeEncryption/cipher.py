from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad
from hashlib import md5
from base64 import b64encode
from itertools import cycle


MD5 = lambda s: md5(s).digest()
KEY_PAD = lambda key: b"\x00" * (16 - len(key)) + key


def custom_encrypt(data, password, keysize):
    data = pad(data, 16)
    def _gen_key(password):
        key = password
        for i in range(1000):
            key = MD5(key)
        return key
    key = bytes_to_long(_gen_key(password))
    ciphers = [
        AES.new(KEY_PAD(long_to_bytes((key*(i+1)) % 2**128)) ,AES.MODE_ECB) for i in range(0, keysize, 16)
    ]
    pt_blocks = [
        data[i:i+16] for i in range(0, len(data), 16)
    ]
    return b64encode(b"".join([cipher.encrypt(pt_block) for pt_block, cipher in zip(pt_blocks, cycle(ciphers))])).decode()
