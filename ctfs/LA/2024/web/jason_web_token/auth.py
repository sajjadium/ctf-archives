import hashlib
import json
import os
import time

secret = int.from_bytes(os.urandom(128), "big")
hash_ = lambda a: hashlib.sha256(a.encode()).hexdigest()


class admin:
    username = os.environ.get("ADMIN", "admin-owo")
    age = int(os.environ.get("ADMINAGE", "30"))


def create_token(**userinfo):
    userinfo["timestamp"] = int(time.time())
    salted_secret = (secret ^ userinfo["timestamp"]) + userinfo["age"]
    data = json.dumps(userinfo)
    return data.encode().hex() + "." + hash_(f"{data}:{salted_secret}")


def decode_token(token):
    if not token:
        return None, "invalid token: please log in"

    datahex, signature = token.split(".")
    data = bytes.fromhex(datahex).decode()
    userinfo = json.loads(data)
    salted_secret = (secret ^ userinfo["timestamp"]) + userinfo["age"]

    if hash_(f"{data}:{salted_secret}") != signature:
        return None, "invalid token: signature did not match data"
    return userinfo, None
