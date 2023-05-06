import enum
import hashlib
import hmac
from typing import NamedTuple

def KMAC(key, size, prefix, content):
    return hashlib.shake_256(key + size.to_bytes(4, byteorder='little') + prefix + content).digest(size)


class RoleLabel(enum.Enum):
    I2R = b'I2R'
    R2I = b'R2I'

class Role(enum.Enum):
    Initiator  = (RoleLabel.R2I, RoleLabel.I2R)
    Responder  = (RoleLabel.I2R, RoleLabel.R2I)


class Context(enum.Enum):
    KEYS = b'\x00'
    ENC = b'\x01'
    INT = b'\x02'

class Counter:
    def __init__(self, init : int = 0) -> None:
        assert init >= 0
        self.val = init
    
    def __call__(self) -> bytes:
        ret = self.val.to_bytes(4, 'big')
        self.val += 1
        return ret

class RoleContext(NamedTuple):
    ENC: bytes
    INT: bytes
    CTR: Counter

def role_ctx_derive(mk: bytes, label: RoleLabel, ctr = 0):
    keys = KMAC(mk, 64, Context.KEYS.value, label.value + b" Session Keys")
    return  RoleContext(keys[:32], keys[32:], Counter(ctr))

def session_context(share : bytes, role: Role):
    mk = hashlib.sha384(share).digest()
    rx_label, tx_label = role.value
    return SessionContext(role_ctx_derive(mk, rx_label), role_ctx_derive(mk, tx_label))

class SessionContext:
    def __init__(self, rx_ctx : RoleContext, tx_ctx : RoleContext):
        self.tx_ctx = tx_ctx
        self.rx_ctx = rx_ctx
    
    def tx_encrypt(self, msg : bytes):
        txc = self.tx_ctx.CTR()
        ct = bytes(x^y for x,y in zip(msg, KMAC(self.tx_ctx.ENC, len(msg), Context.ENC.value, txc)))
        tag = KMAC(self.tx_ctx.INT, 32, Context.INT.value, txc + ct)
        return ct, tag

    def rx_decrypt(self, ct : bytes, tag : bytes):
        rxc = self.rx_ctx.CTR()
        calc_tag = KMAC(self.rx_ctx.INT, 32, Context.INT.value, rxc + ct)
        if not hmac.compare_digest(tag, calc_tag):
                raise RuntimeError("Bad tag")
        return bytes(x^y for x,y in zip(ct, KMAC(self.rx_ctx.ENC, len(ct), Context.ENC.value, rxc)))
