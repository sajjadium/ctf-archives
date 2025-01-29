from random import getrandbits

from Crypto.Util.number import long_to_bytes
from fastapi import APIRouter
from pydantic import BaseModel, validator

from mvmcryption.auth import (
    AdminUser,
    AuthorizedUser,
    GlobalECDSA,
    GlobalSCBCCipher,
)
from mvmcryption.environ import getenv
from mvmcryption.utils import decode, encode

FLAG = getenv("FLAG").encode()

crypto_router = APIRouter(prefix="/crypto", tags=["crypto"])


class DecryptionBody(BaseModel):
    ciphertext: str
    iv: str

    @validator("ciphertext")
    def validate_ciphertext(v):
        try:
            decoded = decode(v)
        except Exception:
            msg = "What exactly are you trying to achieve?"
            raise ValueError(msg)

        if len(decoded) % 16 != 0:
            msg = "????"
            raise ValueError(msg)
        return v

    @validator("iv")
    def validate_iv(v):
        try:
            decoded = decode(v)
            assert len(decoded) == 16
        except Exception:
            msg = "What exactly are you trying to achieve?"
            raise ValueError(msg)
        return v


@crypto_router.get("/public-key")
def ecdsa_public_key(ecdsa: GlobalECDSA) -> dict:
    """ECDSA Public Key."""
    return ecdsa.pretty_public_key


@crypto_router.post("/decrypt")
def decrypt(admin: AdminUser, cipher: GlobalSCBCCipher, body: DecryptionBody):
    """
    Real men test in production.

    - Our CISO, probably
    """

    try:
        res = cipher.decrypt(decode(body.ciphertext), decode(body.iv))
        return {"plaintext": res.decode()}
    except Exception as e:
        return {"err": str(e)}


@crypto_router.get("/flag")
def flag(user: AuthorizedUser, cipher: GlobalSCBCCipher):
    iv = long_to_bytes(getrandbits(128), 16)
    ct = cipher.encrypt(FLAG, iv)
    return {"ciphertext": encode(ct), "iv": encode(iv)}
