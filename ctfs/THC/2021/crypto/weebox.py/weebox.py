import hashlib
import sys

#
# weebox.py
# - written by plcp
# - owned by quarkslab
# - only engages its author for code quality :)
#

nb_bits = 256
nb_bytes = 32
nb_words = 64
word_len = 4
word_mask = (2**word_len) - 1
ladder_size = 2**word_len

group = 115792089210356248762697446949407573530086143415290314195533631308867097853951
order = 115792089210356248762697446949407573529996955224135760342422259061068512044369

#
# finite field arithmetic
#

moduli = None

def invmod(a):
    return pow(a % moduli, moduli - 2, moduli)

def mulmod(a, b):
    return (a * b) % moduli

def doublemod(a):
    return (a + a) % moduli

def addmod(a, b):
    return (a + b) % moduli

def submod(a, b):
    return (moduli + a - b) % moduli

#
# curve arithmetic
#

gptx = 108916722531310784954987870693632311777886073173317798030971327994717526058474
gpty = 48669730670864784357653778404419338261994208753462863646109767832706509632230
gptz = 73235898817912095104913541943786679798085951656820227383958162362143073870143

gpt = (gptx, gpty, gptz)

def to_affine(pt):
    global moduli
    last, moduli = moduli, group

    x, y, z = pt
    iz = invmod(z)
    iz2 = mulmod(iz, iz)
    x = mulmod(x, iz2)
    y = mulmod(y, mulmod(iz2, iz))

    moduli = last
    return (x, y)

def doublept(pt):
    x, y, z = pt

    y2 = mulmod(y, y)
    y4 = mulmod(y2, y2)
    z2 = mulmod(z, z)
    z4 = mulmod(z2, z2)
    x2 = mulmod(x, x)

    s = mulmod(4, mulmod(x, y2))
    m = mulmod(3, submod(x2, z4))
    xd = submod(mulmod(m, m), doublemod(s))
    yd = submod(mulmod(m, submod(s, xd)), mulmod(8, y4))
    zd = doublemod(mulmod(y, z))

    return (xd, yd, zd)

def addpt(pt, other):
    x1, y1, z1 = pt
    x2, y2, z2 = other

    z1p2 = mulmod(z1, z1)
    z2p2 = mulmod(z2, z2)

    u1 = mulmod(x1, z2p2)
    u2 = mulmod(x2, z1p2)

    # mmmh, ignore infinity?
    #
    if u1 == u2:
        return doublept(pt)

    v1 = mulmod(y1, mulmod(z2p2, z2))
    v2 = mulmod(y2, mulmod(z1p2, z1))

    h = submod(u2, u1)
    r = submod(v2, v1)
    h2 = mulmod(h, h)
    h3 = mulmod(h2, h)

    x = submod(submod(mulmod(r, r), h3), doublemod(mulmod(u1, h2)))
    y = submod(mulmod(r, submod(mulmod(u1, h2), x)), mulmod(v1, h3))
    z = mulmod(h, mulmod(z1, z2))

    return (x, y, z)

def negpt(pt):
    global s1, s2, s3
    x, y, z = pt
    return (x, moduli - y, z)

def scalarmult(pt, scalar):
    global moduli
    last, moduli = moduli, group

    ret = None
    mask = 1 << nb_bits
    for _ in range(nb_bits):
        mask >>= 1
        if ret is not None:
            ret = doublept(ret)
        if scalar & mask:
            ret = addpt(ret, pt) if ret is not None else pt

    moduli = last
    return ret

#
# windowing
#

class scalar_table:
    def __init__(self, data, table):
        self.table = table
        self.data = data

    def __call__(self, scalar):
        assert moduli == order
        scalar = scalar % moduli

        words = []
        for _ in range(nb_words):
            words.append(scalar & word_mask)
            scalar >>= word_len

        acc = 0
        for idx in range(nb_words):
            acc = mulmod(ladder_size, acc)
            acc = addmod(acc, self.table[nb_words * words[-1 - idx] + idx])

        return acc

class point_table:
    def __init__(self, data, table):
        self.table = table
        self.data = data

    def __call__(self, scalar):
        global moduli
        last, moduli = moduli, group

        words = []
        for _ in range(nb_words):
            words.append(scalar & word_mask)
            scalar >>= word_len

        acc = self.table[nb_words * words[-1]]
        for idx in range(1, nb_words):
            acc = addpt(acc, self.table[nb_words * words[-1 - idx] + idx])

        moduli = last
        return acc

#
# load tables
#

def load(table):
    ret = []
    for idx in range(1024):
        blob = table[idx * 32:(idx + 1) * 32]
        ret.append(int.from_bytes(blob, byteorder='big'))
    return scalar_table(table, ret)

def loadpt(table):
    ret = []
    for idx in range(1024):
        blob = table[idx * 32 * 3:(idx + 3) * 32 * 3]
        x = int.from_bytes(blob[0:32], byteorder='big')
        y = int.from_bytes(blob[32:64], byteorder='big')
        z = int.from_bytes(blob[64:96], byteorder='big')
        ret.append((x, y, z))
    return point_table(table, ret)

with open('tables.bin', 'rb') as f:
    tables = f.read()

la8b2f19f = load(tables[0:32768])
l193d94fd = load(tables[32768:65536])
lc987ed3a = load(tables[65536:98304])
l73dc1cd1 = load(tables[98304:131072])
la3f31e5b = load(tables[131072:163840])
l0c7dced9 = loadpt(tables[163840:262144])
l676247ea = load(tables[262144:294912])
l23892dfe = load(tables[294912:327680])
lb97b239d = load(tables[327680:360448])
l46939eac = load(tables[360448:393216])
lb9d6a1ea = load(tables[393216:425984])
l31e5930b = load(tables[425984:458752])
lc8891a89 = load(tables[458752:491520])
le06cd15a = load(tables[491520:524288])
l48c04bbb = load(tables[524288:557056])
l342337a4 = load(tables[557056:589824])
ld95bb85f = load(tables[589824:622592])
l58d3310b = load(tables[622592:655360])
l9fd80926 = load(tables[655360:688128])
l2a03fe7a = load(tables[688128:720896])
l4d477f0d = load(tables[720896:753664])
lb23e60f2 = load(tables[753664:786432])
la3472e5f = load(tables[786432:819200])
l5ec41a3a = load(tables[819200:851968])
l5a7b02ce = load(tables[851968:884736])
l74013f60 = load(tables[884736:917504])
l09c92783 = load(tables[917504:950272])
l7ed57829 = load(tables[950272:983040])
l89c6ab42 = load(tables[983040:1015808])

#
# verify
#

def load_pub(pub):
    global moduli
    last, moduli = moduli, group

    x = int.from_bytes(pub, byteorder='big')

    cst = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    x3 = mulmod(mulmod(x, x), x)
    y2 = addmod(submod(x3, mulmod(3, x)), cst)
    yd = pow(y2, (moduli + 1) // 4, moduli)

    pub = addpt(addpt(gpt, (x, yd, 1)), negpt(gpt))

    moduli = last
    return pub

def verify(msg, sig, pub):
    global moduli
    last, moduli = moduli, order

    hashed = hashlib.sha256(msg).digest()

    # load
    #

    r, s = sig[:nb_bytes], sig[nb_bytes:]
    e = int.from_bytes(hashed, byteorder='big') % moduli
    r = int.from_bytes(r, byteorder='big') % moduli
    s = int.from_bytes(s, byteorder='big') % moduli
    pub = load_pub(pub)

    # u1 & u2
    #

    s = invmod(s)
    u1 = mulmod(e, s)
    u2 = mulmod(r, s)

    # point

    moduli = group

    pt = addpt(scalarmult(gpt, u1), scalarmult(pub, u2))
    x, _ = to_affine(pt)

    # is sig valid?
    #
    return (x % order) == r

#
# signature
#

def sign(msg):
    global moduli
    last, moduli = moduli, order

    hashed = hashlib.sha256(msg).digest()

    # compute r
    #

    e = int.from_bytes(hashed, byteorder='big') % order
    ie = invmod(e)

    t0 = la8b2f19f(e) % order
    t1 = l193d94fd(t0) % order
    t2 = mulmod(t1, lc987ed3a(ie))
    t3 = addmod(t2, l73dc1cd1(e))
    t4 = addmod(t3, la3f31e5b(ie))
    t5 = l0c7dced9(t4)

    tmp0 = l676247ea(e) % order
    t6 = scalarmult(t5, mulmod(invmod(tmp0), l23892dfe(e)))
    r, _ = to_affine(t6)

    # compute s
    #

    t7 = lb97b239d(t4) % order
    tmp1 = invmod(t7)

    t8 = mulmod(tmp0, l46939eac(tmp1))
    t9 = mulmod(tmp0, lb9d6a1ea(tmp1))

    ta = mulmod(r, l31e5930b(ie))
    ta = addmod(ta, lc8891a89(mulmod(r, ie)))
    ta = addmod(ta, le06cd15a(ie))
    ta = addmod(ta, mulmod(l48c04bbb(ie), l342337a4(r)))
    ta = addmod(ta, mulmod(ld95bb85f(ie), l58d3310b(r)))
    ta = addmod(ta, mulmod(l9fd80926(r), l2a03fe7a(ie)))

    tb = mulmod(r, l4d477f0d(ie))
    tb = addmod(tb, lb23e60f2(mulmod(r, ie)))
    tb = addmod(tb, la3472e5f(ie))
    tb = addmod(tb, mulmod(l5ec41a3a(ie), l5a7b02ce(r)))
    tb = addmod(tb, mulmod(l74013f60(ie), l09c92783(r)))
    tb = addmod(tb, mulmod(l7ed57829(r), l89c6ab42(ie)))

    s = addmod(mulmod(ta, t8), mulmod(tb, t9))

    # finalize
    #

    r = r.to_bytes(nb_bytes, byteorder='big')
    s = s.to_bytes(nb_bytes, byteorder='big')

    moduli = last
    return r + s

if __name__ == "__main__":
    pub = '9274d0bb1bd842d732a3ddc415032e45efa0130d8140a4fa77e67e284224968e'
    pub = bytes.fromhex(pub)

    msg = b'A specter is haunting the world, the specter of crypto anarchy.'
    sig = sign(msg)
    assert verify(msg, sig, pub)

    if len(sys.argv) != 2:
        print('Usage: {} <hex>'.format(sys.argv[0]))
        sys.exit(1)

    msg = bytes(sys.argv[1], encoding='utf8')
    sig = sign(msg)
    assert verify(msg, sig, pub)

    print('signature:', sig.hex())
    print('public key:', pub.hex())
