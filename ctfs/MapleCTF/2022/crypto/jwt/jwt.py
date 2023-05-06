from Crypto.Util.number import bytes_to_long as bl, inverse
from fastecdsa.curve import secp256k1
from base64 import urlsafe_b64decode, urlsafe_b64encode
from hashlib import sha256
from json import loads, dumps
from secret import private


def b64decode(msg: str) -> bytes:
    if len(msg) % 4 != 0:
        msg += "=" * (4 - len(msg) % 4)
    return urlsafe_b64decode(msg.encode())


def b64encode(msg: bytes) -> str:
    return urlsafe_b64encode(msg).decode().rstrip("=")


class ES256:
    def __init__(self):
        self.G = secp256k1.G
        self.order = secp256k1.q
        self.private = private
        self.public = self.G * self.private

    def _sign(self, msg):
        z = sha256(msg.encode()).digest()
        k = self.private

        z = bl(z)

        r = (k * self.G).x
        s = inverse(k, self.order) * (z + r * self.private) % self.order

        return r, s

    def _verify(self, r, s, msg):
        if not (1 <= r < self.order and 1 <= s < self.order):
            return False

        z = sha256(msg.encode()).digest()
        z = bl(z)

        u1 = z * inverse(s, self.order) % self.order
        u2 = r * inverse(s, self.order) % self.order

        p = u1 * self.G + u2 * self.public

        return r == p.x

    # return true if the token signature matches the data
    def verify(self, data, signature):
        r = int.from_bytes(signature[:32], "little")
        s = int.from_bytes(signature[32:], "little")

        return self._verify(r, s, data)

    # return the signed message and update private/public
    def sign(self, data):
        header = b64encode(
            dumps({"alg": "ES256", "typ": "JWT"}).replace(" ", "").encode()
        )
        data = b64encode(dumps(data).replace(" ", "").encode())

        r, s = self._sign(header + "." + data)
        signature = r.to_bytes(32, "little") + s.to_bytes(32, "little")

        return header + "." + data + "." + b64encode(signature)

    # return the decoded token as a JSON object
    def decode(self, token):
        _header, _data, _signature = token.split(".")
        header = loads(b64decode(_header))
        data = loads(b64decode(_data))
        signature = b64decode(_signature)

        if header["alg"] != "ES256":
            raise Exception("Algorithm not supported!")

        if not self.verify(_header + "." + _data, signature):
            raise Exception("Invalid signature")

        return {"user": data["user"]}


jwt = ES256()
