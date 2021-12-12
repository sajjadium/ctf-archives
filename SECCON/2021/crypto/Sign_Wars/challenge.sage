from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad
import random
from secret import msg1, msg2, flag

flag = pad(flag, 96)
flag1 = flag[:48]
flag2 = flag[48:]

# P-384 Curve
p = 39402006196394479212279040100143613805079739270465446667948293404245721771496870329047266088258938001861606973112319
a = -3
b = 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575
curve = EllipticCurve(GF(p), [a, b])
order = 39402006196394479212279040100143613805079739270465446667946905279627659399113263569398956308152294913554433653942643
Z_n = GF(order)
gx = 26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087
gy = 8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871
G = curve(gx, gy)

for b in msg1:
    assert b >= 0x20 and b <= 0x7f
z1 = bytes_to_long(msg1)
assert z1 < 2^128

for b in msg2:
    assert b >= 0x20 and b <= 0x7f
z2 = bytes_to_long(msg2)
assert z2 < 2^384

# prequel trilogy
def sign_prequel():
    d = bytes_to_long(flag1)
    sigs = []
    for _ in range(80):
        # normal ECDSA. all bits of k are unknown.
        k1 = random.getrandbits(128)
        k2 = z1
        k3 = random.getrandbits(128)
        k = (k3 << 256) + (k2 << 128) + k1
        kG = k*G
        r, _ = kG.xy()
        r = Z_n(r)
        k = Z_n(k)
        s = (z1 + r*d) / k
        sigs.append((r,s))

    return sigs

# original trilogy
def sign_original():
    d = bytes_to_long(flag2)
    sigs = []
    for _ in range(3):
        # normal ECDSA
        k = random.getrandbits(384)
        kG = k*G
        r, _ = kG.xy()
        r = Z_n(r)
        k = Z_n(k)
        s = (z2 + r*d) / k
        sigs.append((r,s))

    return sigs


def sign():
    sigs1 = sign_prequel()
    print(sigs1)
    sigs2 = sign_original()
    print(sigs2)


if __name__ == "__main__":
    sign()