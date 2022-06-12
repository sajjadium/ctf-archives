import json
import hashlib
from fastecdsa.curve import P192 as Curve
from fastecdsa.point import Point

from secrets import randbits

from server_config import flag

N = Curve.q.bit_length()

registered_keys = {}

def read() -> dict:
    return json.loads(input())

def write(m : dict):
    print(json.dumps(m))

def parse_ec(p):
    return Point(int(p[0], 16), int(p[1], 16), Curve)

def generate_nonce():
    sk = randbits(N)
    return sk, sk*Curve.G

def mod_hash(msg : bytes, R : Point) -> int:
    h = hashlib.sha256()
    h.update(len(msg).to_bytes(64, 'big'))
    h.update(msg)
    h.update(R.x.to_bytes(N//8, 'big'))
    h.update(R.y.to_bytes(N//8, 'big'))
    return int(h.hexdigest(), 16) % Curve.q

def verify(pubkey : Point, m : bytes, z : int, c : int) -> bool:
    R = z*Curve.G - c * pubkey
    return c == mod_hash(m, R)

def coords(p : Point) -> (str, str):
    return (hex(p.x)[2:], hex(p.y)[2:])

def genkey():
    sk, server_share = generate_nonce()
    write({"pubkey_share": coords(server_share)})
    pk = read()["pubkey_share"]
    client_share = parse_ec(pk)
    public_key = server_share + client_share
    registered_keys[public_key] = sk
    write({"registered":coords(public_key)})


def sign(pubkey : Point):
    if pubkey not in registered_keys:
        write({"error": "Unknown pubkey"})
        return
    secret_key = registered_keys[pubkey]
    secret_nonce, public_nonce = generate_nonce()
    write({"D": coords(public_nonce)})
    response = read()
    client_nonce = parse_ec(response["D"])
    msg = bytes.fromhex(response["msg"])
    R = public_nonce + client_nonce
    if (msg == b"Gimme!"):
        write({"error":"No way Jose!"})
        return
    c = mod_hash(msg, R)
    z = secret_nonce + secret_key * c
    write({"z":hex(z)[2:]})

def serve():
    try:
        write({"banner": "Welcome to Frosty's Snowman Signing Server. Choose an option: genkey, sign or verify"})
        msg = read()
        if msg["op"] == "genkey":
            genkey()
        elif msg["op"] == "sign":
            sign(parse_ec(msg["pubkey"]))
        elif msg["op"] == "verify":
            m = bytes.fromhex(msg["m"])
            z = int(msg["z"], 16)
            c = int(msg["c"], 16)
            pubkey = parse_ec(msg["pubkey"])
            verified = verify(pubkey, m, z, c)
            write({"verified": verified})
            if verified and m == b'Gimme!':
                write({"flag": flag})
    except (ValueError, KeyError, TypeError, json.decoder.JSONDecodeError):
        write({"error": "Invalid input"})

if __name__ == "__main__":
    while True:
        serve()
