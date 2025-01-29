from dataclasses import dataclass
from json import dumps, loads

from mvmcryption.utils import decode as b64decode
from mvmcryption.utils import encode as b64encode

from .ecdsa import ECDSA, decode_signature, encode_signature

# SJWT -> Scuffed JSON Web Token; just some extra pain


class SJWTError(ValueError):
    """Error for SJWT things."""


class SJWTEncodingError(SJWTError):
    """Errors for encoding SJWTs!"""


class SJWTDecodeError(SJWTError):
    """Shit happend while decoding that SJWT!"""


class SJWTVerificationError(SJWTError):
    """That SJWT nasty!"""


@dataclass
class SJWT:
    ecdsa: ECDSA

    def encode(self, payload: dict[str], requires_expiry=True) -> str:
        if "exp" not in payload and requires_expiry:
            raise SJWTEncodingError("Sir we need an expiry on the token!")
        as_string = dumps(payload)
        _body = as_string.encode()
        sig = encode_signature(self.ecdsa.sign(_body))
        body = b64encode(_body)

        return body + "." + sig

    def decode(self, string: str, verify: bool = True) -> dict[str]:
        parts = string.split(".")
        if len(parts) != 3:
            # why even try this >:(
            raise SJWTDecodeError("WRONG AMOUNT OF parts! parts! >:C")
        try:
            body = b64decode(parts[0])
            r, s = decode_signature(parts[1:])
        except Exception:
            # JUST STOP IT; THIS IS SECURE!!!!!! >:C
            raise SJWTDecodeError("Bad token! bad bad bad!")
        if verify:
            self._verify(body, (r, s))
        try:
            return loads(body.decode())
        except Exception:
            raise SJWTDecodeError("funny user")

    def _verify(self, body: bytes, signature: tuple[int, int]) -> None:
        # raise if payload not satisfactory
        if not (self.ecdsa.verify(signature, body)):
            raise SJWTVerificationError(":c stop it")
