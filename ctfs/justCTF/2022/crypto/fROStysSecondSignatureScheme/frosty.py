import json
import hashlib
from fastecdsa.curve import P192 as Curve
from fastecdsa.point import Point

from secrets import randbits

from server_config import flag, server_privkey_share, client_pubkey_share

N = Curve.q.bit_length()
server_pubkey_share = server_privkey_share * Curve.G
pubkey = client_pubkey_share + server_pubkey_share

def read() -> dict:
    return json.loads(input())

def write(m : dict):
    print(json.dumps(m))

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


def sign():
    secret_nonce, public_nonce = generate_nonce()
    write({"D": coords(public_nonce)})
    response = read()
    (dx, dy) = response["D"]
    msg = bytes.fromhex(response["msg"])
    client_nonce = Point(int(dx, 16), int(dy, 16), Curve)
    R = public_nonce + client_nonce
    if (msg == b"Gimme!"):
        write({"error":"No way Jose!"})
        return
    c = mod_hash(msg, R)
    z = secret_nonce + server_privkey_share * c
    write({"z":hex(z)[2:]})

def serve():
    try:
        write({"banner": "Welcome to Very Frosty's Snowman Signing Server. Choose an option: sign or verify"})
        msg = read()
        if msg["op"] == "sign":
            sign()
        elif msg["op"] == "verify":
            m = bytes.fromhex(msg["m"])
            z = int(msg["z"], 16)
            c = int(msg["c"], 16)
            verified = verify(pubkey, m, z, c)
            write({"verified": verified})
            if verified and m == b'Gimme!':
                write({"flag": flag})
    except (ValueError, KeyError, TypeError, json.decoder.JSONDecodeError):
        write({"error": "Invalid input"})

if __name__ == "__main__":
    serve()
