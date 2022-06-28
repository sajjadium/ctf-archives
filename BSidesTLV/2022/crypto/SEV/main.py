import enum
import sys

from hashlib import sha256

from ecdsa.ellipticcurve import PointJacobi
from ecdsa.curves import NIST384p, NIST256p
from ecdsa.ecdh import ECDH
from ecdsa.keys import SigningKey, VerifyingKey

from lib.session import session_context, Role
from lib.io import IO 
from lib.pow import PoW

def log(msg):
    print(msg, file=sys.stderr)

class Curve(enum.IntEnum):
    p256 = 1
    p384 = 2

curve_map = {
    Curve.p256: NIST256p.curve,
    Curve.p384: NIST384p.curve,
}

def validate_point(curve : Curve, x : int, y : int):
    return curve_map[curve.value].contains_point(x, y)


def read_private_key():
    with open('private.key', 'rb') as f:
        return f.read()

@IO
class io:
    def writeLine(line : bytes):
        log(f"Write: {line.decode('latin1')}")        
        sys.stdout.buffer.write(line + b'\n')
        sys.stdout.buffer.flush()

    def readLine():
        line = sys.stdin.buffer.readline()[:-1]
        log(f"Read: {line.decode('latin1')}")
        return line


def send_debug(ecdh, ctx):
    res = ecdh.public_key.pubkey.point * ecdh.private_key.privkey.secret_multiplier
    io.writeData(*ctx.tx_encrypt(res.to_bytes()))
    ctx.tx_ctx.CTR.val = 0

def session(ecdh : ECDH, role : Role, debug = False):
    ctx = session_context(ecdh.generate_sharedsecret_bytes(), role)
    id = sha256(ecdh.public_key.to_string()).digest()
    if debug:
        send_debug(ecdh, ctx)
    try:
        io.writeData(*ctx.tx_encrypt(f"Welcome your pub fingerprint is {id.hex()}".encode('latin1')))
        while True:
            msg = ctx.rx_decrypt(*io.readData())
            io.writeLine(f"You are forgiven for sin confessed having sha256 digest: {sha256(msg).hexdigest()}".encode('latin1'))
    except BaseException as e:
        log(f'Confession Session error: {e}')
    io.writeLine(b"Confession Session ended")


def main():
    sk : SigningKey = SigningKey.from_der(read_private_key())
    ecdh = ECDH(private_key=sk)
    pk : VerifyingKey = ecdh.get_public_key()
    io.writeData(pk.to_string())
    
    while True:
        pow = PoW()
        nonce, tag = pow.generate()
        io.writeLine(f"Provide PoW to be forgiven: {pow.hashFn().name}(secret || nonce) == tag".encode('latin1'))
        io.writeLine(f"Where len(secret) is {pow.lvl}. nonce and tag are provided as data:".encode('latin1'))
        io.writeData(nonce, tag)
        pow_answer, = io.readData()
        if not pow.validate(pow_answer, tag):
            io.writeLine(b"Error: Bad proof. You will not be forgiven.")
            continue
        manifest = io.readData()
        assert len(manifest) == 3, f'Manifest should contain 3 elements: curve|x|y'
        curve, x, y = manifest
        assert len(curve) == 1 and len(x) == len(y) == 80, f'Manifest elements format expected(got): curve 1({len(curve)}) byte, x: 80({len(x)}) bytes, y: 80({len(y)}) bytes'
        curve, x, y = Curve(int.from_bytes(curve, 'big')), int.from_bytes(x, 'big'), int.from_bytes(y, 'big')
        if not validate_point(curve, x, y):
            io.writeLine(f"Invalid point ({x}, {y}) for curve {curve.name}")
            continue
        ecdh.load_received_public_key(VerifyingKey.from_public_point(PointJacobi(sk.curve.curve, x, y, 1), curve=sk.curve, validate_point=False))
        session(ecdh, Role.Responder, debug=curve == Curve.p256)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        io.writeLine(str(e).encode())
    finally:
        sys.stdin.close()
        sys.stdout.close()
    
