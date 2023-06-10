#!/usr/bin/env sage

import sys
from secrets import key1, key2 # file secrets.py
from sage.all import *
from Crypto.Util.number import *

if len(sys.argv) != 2:
    print("Usage: %s <message>" % sys.argv[0])
    print("Returns the signature for the message given.")
    sys.exit(1)

p = 0x23FFFFFDC000000D7FFFFFB8000001D3FFFFF942D000165E3FFF94870000D52FFFFDD0E00008DE55C00086520021E55BFFFFF51FFFF4EB800000004C80015ACDFFFFFFFFFFFFECE00000000000000067
K = GF(p)
a = K(0)
b = K(0x101)
E = EllipticCurve(K, (a, b))
G = E(p-1, 0x10)
o = 0x23FFFFFDC000000D7FFFFFB8000001D3FFFFF942D000165E3FFF94870000D52FFFFDD0E00008DE55600086550021E555FFFFF54FFFF4EAC000000049800154D9FFFFFFFFFFFFEDA00000000000000061
E.set_order(o)

msg = int.from_bytes(bytes(sys.argv[1], 'utf-8'), 'big')
if (Integer(msg).nbits() > o.nbits()):
    print("Message too long!")
    sys.exit(1)

pt = key1*G
r = mod(pt[0],o)
s = mod(pow(key1,-1,o)*(msg+r*key2),o)
print(f'Signature: ({r}, {s})')