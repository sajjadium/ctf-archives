import ecdsa, ecdsa.ecdsa
from cryptography.hazmat.primitives.kdf.kbkdf import (
   CounterLocation, KBKDFHMAC, Mode
)
from cryptography.hazmat.primitives import hashes
import secrets
from Crypto.Cipher import ChaCha20_Poly1305

def get_order(): return ecdsa.NIST256p.generator.order()
def encrypt_sym(input_bytes: bytes, key:bytes):

    cipher = ChaCha20_Poly1305.new(key=key)
    ciphertext, tag = cipher.encrypt_and_digest(input_bytes)
    return ciphertext + tag + cipher.nonce

def derive_symkey(inp:bytes):
    kdf = KBKDFHMAC(
        algorithm=hashes.SHA3_256(),
        mode=Mode.CounterMode,
        length=32,
        rlen=4,
        llen=4,
        location=CounterLocation.BeforeFixed,
        label=b"safu",
        context=b"funds are safu",
        fixed=None,
    )
    return kdf.derive(inp)
    
def make_keys():
    gen = ecdsa.NIST256p.generator
    secret = secrets.randbelow(gen.order()-1) + 1
    pub_key = ecdsa.ecdsa.Public_key(gen, gen * secret)
    priv_key = ecdsa.ecdsa.Private_key(pub_key, secret)
    return priv_key, pub_key

def int_to_bytes(n: int) -> bytes:
    return n.to_bytes((n.bit_length() + 7) // 8, 'big') or b'\0'

def encrypt(kpub_dest:ecdsa.ecdsa.Public_key, msg:str):
    gen = ecdsa.NIST256p.generator
    r = secrets.randbelow(gen.order()-1) + 1
    R = gen * r
    S = kpub_dest.point * r
    key = derive_symkey(int_to_bytes(int(S.x())))
    cp = encrypt_sym(msg.encode(), key).hex() 
    return cp + "deadbeef" + R.to_bytes().hex()

