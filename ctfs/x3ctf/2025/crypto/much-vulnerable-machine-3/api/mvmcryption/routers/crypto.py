from datetime import datetime

from fastapi import APIRouter
from pydantic import BaseModel, validator

from mvmcryption.auth import (
    AuthorizedUser,
    GlobalECDSA,
    GlobalRSA,
    GlobalXSCBCCipher,
)
from mvmcryption.environ import getenv
from mvmcryption.utils import decode, encode

FLAG = getenv("FLAG").encode()

crypto_router = APIRouter(prefix="/crypto", tags=["crypto"])


class ValidationBody(BaseModel):
    ciphertext: str
    iv: str
    signature: str
    debug: bool = False

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

    @validator("signature")
    def validate_signature(v):
        try:
            decoded = int(v, 16)
            assert decoded > 1
        except Exception:
            msg = "What exactly are you trying to achieve?"
            raise ValueError(msg)
        return v


@crypto_router.get("/public-key")
def ecdsa_public_key(ecdsa: GlobalECDSA) -> dict:
    """ECDSA Public Key."""
    return ecdsa.pretty_public_key


@crypto_router.get("/rsa-public-key")
def rsa_public_key(_user: AuthorizedUser, rsa: GlobalRSA) -> dict:
    """RSA Public Key."""

    return {
        "N": hex(rsa.priv.n),
        "e": hex(rsa.priv.e),
    }


@crypto_router.post("/decrypt")
def decrypt(user: AuthorizedUser, cipher: GlobalXSCBCCipher, body: ValidationBody):
    """
    Real men test in production.

    - Our CISO, probably
    """

    if body.debug:
        if not user.is_admin:
            raise ValueError("no.")
    try:
        res = cipher.decrypt(
            decode(body.ciphertext), int(body.signature, 16), decode(body.iv)
        )
        user.send_email(
            f"Decryption Results from {datetime.now().isoformat()}",
            f"Plaintext = {res!r}",
        )
        return {}
    except Exception as e:
        if body.debug:
            return {"err": str(e)}
        return {}


@crypto_router.get("/flag")
def flag(user: AuthorizedUser, cipher: GlobalXSCBCCipher):
    ct, signature = cipher.encrypt(FLAG)
    return {"ciphertext": encode(ct), "signature": hex(signature)}
