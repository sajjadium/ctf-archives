#!/usr/bin/env python3
# coding: utf-8
# 外国人想法真是不一样
import base64
import ctypes
import importlib
import os
import struct
import sys
import zlib
from Crypto.Cipher import AES
from hashlib import md5
assert sys.maxsize > 9876543210, 'Can\'t run on a steam engine :('
assert sys.platform[0] == 'l', 'Software update required'
sys.excepthook=lambda*_:os._exit(0)

FLAGS = [False, True, True, False, True]
NOPE = []

flags = {}
def flag(y):
    def flag(x, z):
        try: 0/0
        except Exception as e: flag = e.__traceback__.tb_frame.f_back.f_lineno
        flags[flag] = flag = f'{x}{y}{z}'
        return Flag(flag)
    return flag

class Flag(str):
    __getattr__  = flag('.')
    __matmul__   = flag('@')
    __sub__      = flag('-')
    __floordiv__ = flag('!')

FLAG,FLAG = os.path.splitext(os.path.basename(sys.modules['__main__'].__file__))[::-1]
while True:
    try:
        importlib.import_module(FLAG) ; break
    except NameError as flag:
        _, flag, _ = flag.args[0].split("'")
        globals()['__builtins__'][flag] = Flag(flag)

flag = ctypes.CDLL(None).mmap
flag.restype = ctypes.c_long
flag.argtypes = (ctypes.c_long,) * 6
def galf(p):
    return ctypes.cast(p, ctypes.c_voidp).value
Flag = ctypes.cast(flag(0, 1<<32, 3, 16418, -1, 0), ctypes.POINTER(ctypes.c_ubyte))
fLag = ctypes.cast(flag(0, 1<<33, 7, 16418, -1, 0), ctypes.POINTER(ctypes.c_ubyte))
flAg = ctypes.cast(flag(0, 1<< 6, 3, 16418, -1, 0), ctypes.POINTER(ctypes.c_uint32))
flaG = ctypes.cast(flag(0, 1<< 7, 3, 16418, -1, 0), ctypes.POINTER(ctypes.c_voidp))
FLAG =             flag(0, 1<< 7, 7, 16418, -1, 0)

aes = AES.new(md5(open(__file__, 'rb').read()).digest(), AES.MODE_ECB)
for i, (_, x) in enumerate(sorted(flags.items()), 0x2ab):
    a, b = x.split('!')
    o = int(bytes(a, 'utf8').hex(), 16) % 7
    x = int(aes.decrypt(bytes.fromhex(b)).hex(), 16)
    y = [o]
    for _ in range(5 + (o==6)):
        y.append(x & 0xff) ; x >>= 8
    xs = y[o==6:]
    for j, x in enumerate(xs):
        Flag[i*6+j] = x
flAg[15] = 0x1002

def in_(i):    return Flag[i & 0xffffffff] if i > 0xfff else os._exit(1)
def out(i, x): Flag[i & 0xffffffff] = x & 0xff if i > 0xfff else os._exit(1)
def IN_(i):    return flAg[i & 0xf]
def OUT(i, x): flAg[i & 0xf] = x
def inn(a):    x=in_;return x(a),x(a+1)&15,x(a+1)>>4,x(a+2)|x(a+3)<<8|x(a+4)<<16|x(a+5)<<24

def flag(truth):
    res = {}
    while truth[0] != 0:
        n = 0
        i = 0
        while True:
            b = truth.pop(0)
            n |= (b & 0x7f) << i * 7
            i += 1
            if not b & 0x80:
                break
        off = n - 2
        if truth[0] == 1:
            truth.pop(0)
            n = 0
            i = 0
            while True:
                b = truth.pop(0)
                n |= (b & 0x7f) << i * 7
                i += 1
                if not b & 0x80:
                    break
            sz = n - 2
            rec = (sz, flag(truth))
        else:
            rec = flag(truth)
        res[off] = rec
    truth.pop(0)
    return res
def recurse(addr, sig, n):
    if isinstance(sig, tuple):
        sz, sig = sig
        while recurse(addr, sig, n):
            addr += sz
    else:
        ret = False
        for off, sub in sig.items():
            x = (
                Flag[addr + off] |
                Flag[addr + off + 1] << 8 |
                Flag[addr + off + 2] << 16 |
                Flag[addr + off + 3] << 24 |
                Flag[addr + off + 4] << 32 |
                Flag[addr + off + 5] << 40 |
                Flag[addr + off + 6] << 48 |
                Flag[addr + off + 7] << 56
            )
            if 0x1000 <= min(x, x + n) < 2**32:
                recurse(min(x, x + n), sub, n)
                Flag[addr + off] = (x + n) & 0xff
                Flag[addr + off + 1] = ((x + n) >> 8) & 0xff
                Flag[addr + off + 2] = ((x + n) >> 16) & 0xff
                Flag[addr + off + 3] = ((x + n) >> 24) & 0xff
                Flag[addr + off + 4] = ((x + n) >> 32) & 0xff
                Flag[addr + off + 5] = ((x + n) >> 40) & 0xff
                Flag[addr + off + 6] = ((x + n) >> 48) & 0xff
                Flag[addr + off + 7] = ((x + n) >> 56) & 0xff
                ret = True
        return ret
_syscall = ctypes.CDLL(None).syscall
_syscall.restype = ctypes.c_long
_syscall.argtypes = (ctypes.c_long,) * 6
def do_syscall(nr, argsaddr):
    argsaddr &= 0xffffffff
    flag = do_syscall.flag.get(nr, {})
    recurse(argsaddr, flag, galf(Flag))
    args = struct.unpack('<QQQQQQ', bytes(Flag[argsaddr : argsaddr + 6 * 8]))
    ret = _syscall(nr, *args)
    recurse(argsaddr, flag, -galf(Flag))
    return ret
do_syscall.flag=flag(bytearray(zlib.decompress(base64.b85decode('''c$`&KTW^g)6x\
}nQ6yF1K+)v^~LZoqxxIKu72fPU4PDB(*e?Ub%q18LuCOo(#+J<tpT12W^)l#%XBZwD?AaMziw64L6w\
f6odagwvwUbAQI*?VTbIX)JNU_-n}ju)_@uwlxEBQ`SjQsYEY=44bXDUs2b9RnL1J4}d-OZ<4i1lUBX\
(lS|O64X<4wW+Xanw<-qj?oMq&5Ws=Ma&hMje03v3_+QbHJXc@d73j{aY0&SA#9OWT8t_VdL$5KNsJC\
;Dd;lfEr+dutwi1`#8!i^fnN(-r~R!5+W^}L+oX}rU|W=JRosU0cGwQsPL1TjcENTdvImwAUI5z*+eZ\
be?N9tc2f-nij0zo~h@oN)NeOv{@k$4%B2*J<s69b;#^!6Otz)2`>>S~|O*JG1a3B{LzDURrE;$@WBU\
uyS3INMqCGQMf-43M7sp}5oJAvG_i5{zV&)j{s^1yhnxju#-aq-9OzMt@fv8PUN>lp*jZLt@Oza+eJd\
TFmM{>JemlDC|BM|e;8K=^1=pIq!l<nXrTvr7m1#abAkaM1WyIOxBzq3=$=xF1>z<R^8%tmJQ}NB1Xe\
_irEvJVb?rBEn%pF`>lke5tuIhRVI}qQYFI*MmM{f}<21BUJhDNbuQLs|f1jmUPn8r+nBSnmWy_vtDJ\
j<aH*hCvWh)Y@fWtOdyR6H~Igc5q`}c&|)iHWA^ndg|zx)*Ef=N(zaS#_OP9)9fVtiPHVl3CA$ed>`x\
zK+MZ;uDf&Wp4+H7<dL;v4JQzr6lvS}TdsrUvm?OQ#OoV<f^RKKq(kd+xzw*d7$#`p|duk)UnJgsjQ8\
-~;rNeUN9~&oviv'''))))

def magic(*some_arguments):
    def less_magic(some_function):
        global FLAG
        @ctypes.CFUNCTYPE(None, ctypes.c_long)
        def another_function(x):
            try:
                # XXX: Here be dragons?
                y = (x - 5 - galf(fLag)) // 2
                OUT(15, y)
                some_function()
                OUT(0, 0)
            except:
                os._exit(0)
        sys.argv.append(another_function) # Won't work without... ¯\_(ツ)_/¯
        flag = b''.join((
            b'\x55\x48\x89\xe5\x48\x83\xe4\xf0\x48\xb8',
            another_function,
            b'\xff\xd0\xc9',
            *some_arguments,
            b'\xc3',
        ))
        ctypes.memmove(FLAG, flag, len(flag))
        FLAG += len(flag)
        return ctypes.cast(FLAG - len(flag), ctypes.CFUNCTYPE(None))
    return less_magic

def more_magic(normal_amount_of_magic):
    cigam_fo_tnuoma_lamron = galf(normal_amount_of_magic)
    x = 0
    while True:
        if cigam_fo_tnuoma_lamron == flaG[x]:
            break
        x += 1
    return b'\xe8\x00\x00\x00\x00\x5f\x41\xff\x55' + bytes([x<<3])

def this(x, xs, force=False):
    assert not FLAGS[3] or x % 6 == 0
    if fLag[2*x] and not force:
        return
    xs = xs.ljust(12, b'\x90')
    assert len(xs) == 12
    y = x * 2 + galf(fLag)
    ctypes.memmove(y, xs, len(xs))

@magic(
    b'\x48\xbb' + flAg,
    b'\x49\xbc' + Flag,
    b'\x49\xbd' + flaG,
    b'\x49\xbe' + fLag,
    b'\x49\x8d\x86\x04\x20\x00\x00',
    b'\xff\xe0',
)
def entry():
    pass # lol wat?

def p32(x):
    return struct.pack('<I', x % 2**32)

@magic(b'\x48\x83\x2c\x24\x0a')
def thing():
    x = IN_(15)

    if FLAGS[0]:
        this(x, more_magic(device), force=True)
        return

    o, a, b, c = inn(x)
    o_, a_, b_, c_ = inn(x + 6)
    if a:
        wa = b'\x89\x43' + bytes([a*4])
    else:
        wa = b''

    y1 = x + 6
    y2 = None

    magic = more_magic(device)

    if o == 0: magic = more_magic(action)
    elif o == 5 and a == b == 15:
        y1 = y = (x + 6 + c) % 2**32
        z = (6 + c) * 2 - 5
        magic = b'\xe9' + p32(z)
    elif (o == 5 and (a, b, c) == (14, 15, 3) and
          o_ == 5 and a_ == b_ == 15) and FLAGS[1]:
        ra = x + 9
        y1 += 6
        y2 = y = (x + 6 + 6 + c_) % 2**32
        z = (6 + 6 + c_) * 2 - 7 - 5
        magic = b'\xc7\x43\x38' + p32(ra) + b'\xe8' + p32(z)
        this(x + 6, b'\xeb\x0a')
    elif o == 5 and (a, b, c) == (15, 14, 3) and FLAGS[1]: magic = b'\xc3'
    elif (o == 5 and (a, b, c) == (13, 13, 2**32-4) and
          o_ == 3 and a_ != 15 and b_ == 13 and c_ == 3) and FLAGS[2]:
        magic = b'\x83\x6b\x34\x04\x8b\x43' + bytes([a_*4]) + b'\x50'
        y1 += 6
        this(x + 6, b'\xeb\x0a')
    elif (o == 2 and a != 15 and b == 13 and c == 3 and
          o_ == 5 and (a_, b_, c_) == (13, 13, 4)) and FLAGS[2]:
        magic = b'\x83\x43\x34\x04\x58\x89\x43' + bytes([a*4])
        y1 += 6
        this(x + 6, b'\xeb\x0a')
    elif (o, a, b, c) == (4, 0, 0, 3): magic = more_magic(gadget)
    elif 15 not in (a, b):
        if o == 1:
            y2 = y = (x + 6 + c) % 2**32
            z = (6 + c) * 2 - 3 - 3 - 6
            magic = (
                b'\x8b\x43' + bytes([a*4]) +
                b'\x3b\x43' + bytes([b*4]) +
                b'\x0f\x82' + p32(z)
            )
        elif o == 5:
            magic = (
                b'\x8b\x43' + bytes([b*4]) +
                b'\x05' + p32(c) + wa
            )
        elif o == 2:
            magic = b'\x8b\x43' + bytes([b*4]) + b'\x41'
            if c == 0:   magic += b'\x0f\xb6'
            elif c == 1: magic += b'\x0f\xb7'
            else:        magic += b'\x8b'
            magic += b'\x04\x04\x89\x43' + bytes([a*4])
        elif o == 3:
            magic = (
                b'\x8b\x43' + bytes([b*4]) +
                b'\x8b\x4b' + bytes([a*4])
            )
            if c == 0:   magic += b'\x41\x88'
            elif c == 1: magic += b'\x66\x41\x89'
            else:        magic += b'\x41\x89'
            magic += b'\x0c\x04'

        elif o == 4:
            magic = b'\x8b\x43' + bytes([a*4])
            magic += [
                b'\x03\x43' + bytes([b*4]),
                b'\x2b\x43' + bytes([b*4]),
                b'\xf7\x63' + bytes([b*4]),
                b'\x31\xd2\xf7\x73' + bytes([b*4]),
                b'\x31\xd2\xf7\x73' + bytes([b*4]) + b'\x92',
                b'\x23\x43' + bytes([b*4]),
                b'\x0b\x43' + bytes([b*4]),
                b'\x33\x43' + bytes([b*4]),
                b'\x8b\x4b' + bytes([b*4]) + b'\xd3\xe0',
                b'\x8b\x4b' + bytes([b*4]) + b'\xd3\xe8',
                b'\xf7\xd8',
                b'\xf7\xd0',
            ][c]
            magic += b'\x89\x43' + bytes([a*4])

    this(x, magic, force=True)
    for y in (y1, y2):
        if y:
            this(y, more_magic(thing))

@magic(b'\x8b\x43\x3c\x48\x01\xc0\x4c\x01\xf0\x48\x89\x04\x24')
def device():
    x = IN_(15)
    o, a, b, c = inn(x)
    OUT(15, x + 6)

    if o == 0: OUT(a, do_syscall(IN_(b) + c, IN_(a)))
    elif o == 1:
        if IN_(a) < IN_(b): OUT(15, IN_(15) + c)
    elif o == 2:
        y = IN_(b)
        x = in_(y)
        if c > 0:
            x |= in_(y + 1) << 8
        if c > 1:
            x |= in_(y + 2) << 16
            x |= in_(y + 3) << 24
        OUT(a, x)
    elif o == 3:
        x = IN_(a)
        y = IN_(b)
        out(y, x)
        if c > 0:
            out(y + 1, x >> 8)
        if c > 1:
            out(y + 2, x >> 16)
            out(y + 3, x >> 24)
    elif o == 4:
        r = [
            lambda a, b: a + b,
            lambda a, b: a - b,
            lambda a, b: a * b,
            lambda a, b: a // b,
            lambda a, b: a % b,
            lambda a, b: a & b,
            lambda a, b: a | b,
            lambda a, b: a ^ b,
            lambda a, b: a << b,
            lambda a, b: a >> b,
            lambda a, b: -a,
            lambda a, b: ~a,
        ][c](IN_(a), IN_(b))
        OUT(a, r)
    elif o == 5: OUT(a, IN_(b) + c)
    else: os._exit(0)

    this(IN_(15), more_magic(thing))

@magic(b'\xcc')
def gadget():
    os._exit(0)

@magic()
def action():
    _, a, b, c = inn(IN_(15))
    nr = IN_(b) + c
    if nr in NOPE:
        OUT(a, 0xffffefff)
    else:
        OUT(a, do_syscall(nr, IN_(a)))

flaG[0] = galf(thing)
flaG[1] = galf(device)
flaG[2] = galf(gadget)
if not FLAGS[4]:
    flaG[3] = galf(action)
this(0x1002, more_magic(thing))
entry()
