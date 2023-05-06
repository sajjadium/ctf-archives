import itertools
from time import perf_counter_ns as timer
from time import monotonic_ns as timestamp


class Rijndael:
    sbox = bytes.fromhex(
        "637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b27509832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cfd0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdbe0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9ee1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16"
    )
    sboxinv = bytes.fromhex(
        "52096ad53036a538bf40a39e81f3d7fb7ce339829b2fff87348e4344c4dee9cb547b9432a6c2233dee4c950b42fac34e082ea16628d924b2765ba2496d8bd12572f8f66486689816d4a45ccc5d65b6926c704850fdedb9da5e154657a78d9d8490d8ab008cbcd30af7e45805b8b34506d02c1e8fca3f0f02c1afbd0301138a6b3a9111414f67dcea97f2cfcef0b4e67396ac7422e7ad3585e2f937e81c75df6e47f11a711d29c5896fb7620eaa18be1bfc563e4bc6d279209adbc0fe78cd5af41fdda8338807c731b11210592780ec5f60517fa919b54a0d2de57a9f93c99cefa0e03b4dae2af5b0c8ebbb3c83539961172b047eba77d626e169146355210c7d"
    )

    def __init__(self, key):
        self.cache = {}
        self.key = tuple(key)
        keylen = len(key)
        if keylen == 16:
            self.rounds = 10
        elif keylen == 24:
            self.rounds = 12
        elif keylen == 32:
            self.rounds = 14
        else:
            raise ValueError("bad key length")
        rcon = [(0, 0, 0, 0), (1, 0, 0, 0)]
        for i in range(10):
            rcon.append(self.Multiply((2, 2, 2, 2), rcon[-1]))
        N = keylen // 4
        w = []
        for i in range(4 * (self.rounds + 1)):
            if i < N:
                w.append(self.key[4 * i :][:4])
            elif i % N == 0:
                w.append(
                    self.Add(
                        w[-N], self.Add(self.SubWord(self.RotWord(w[-1])), rcon[i // N])
                    )
                )
            elif N > 6 and i % N == 4:
                w.append(self.Add(w[-N], self.SubWord(w[-1])))
            else:
                w.append(self.Add(w[-N], w[-1]))
        self.roundkeys = tuple(w)

    def instance_method_cache(f):
        # lru_cache uses the same cache for every instance which kinda sucks
        # so i made my own cache implementation
        def wrapper(self, *args):
            key = (f.__name__, *args)
            try:
                return self.cache[key][0]
            except TypeError:
                # deal with unhashable arguments
                return f(self, *args)
            except KeyError:
                # remove the least recently used element
                # dont want the cache blowing up
                while len(self.cache.keys()) >= 300:
                    mintimestamp = timestamp()
                    keys = list(self.cache.keys())
                    lowest = -1
                    for i in range(len(keys)):
                        if self.cache[keys[i]][1] < mintimestamp:
                            mintimestamp = self.cache[keys[i]][1]
                            lowest = i
                        else:
                            continue
                    del self.cache[keys[lowest]]
                ret = f(self, *args)
                self.cache[key] = (ret, timestamp())
                return ret

        return wrapper

    @instance_method_cache
    def encrypt(self, m):
        try:
            return b"".join(
                self.encrypt_block(m[i:][:16]) for i in range(0, len(m), 16)
            )
        except:
            return b"Error"

    @instance_method_cache
    def decrypt(self, m):
        try:
            return b"".join(
                self.decrypt_block(m[i:][:16]) for i in range(0, len(m), 16)
            )
        except:
            return b"Error"

    @instance_method_cache
    def encrypt_block(self, block):
        m = tuple(tuple(block[4 * i :][:4]) for i in range(4))
        m = self.Add(self.roundkeys[:4], m)
        for i in range(1, self.rounds):
            m = tuple(self.SubWord(l) for l in m)
            m = self.ShiftRows(m)
            m = self.MixColumns(m)
            m = self.Add(self.roundkeys[4 * i :][:4], m)
        m = tuple(self.SubWord(l) for l in m)
        m = self.ShiftRows(m)
        m = self.Add(self.roundkeys[-4:], m)
        return bytes(itertools.chain.from_iterable(m))

    @instance_method_cache
    def decrypt_block(self, block):
        m = tuple(tuple(block[4 * i :][:4]) for i in range(4))
        m = self.Add(m, self.roundkeys[-4:])
        m = self.ShiftRowsInv(m)
        m = tuple(self.SubWordInv(l) for l in m)
        for i in range(self.rounds - 1, 0, -1):
            m = self.Add(m, self.roundkeys[4 * i :][:4])
            m = self.MixColumnsInv(m)
            m = self.ShiftRowsInv(m)
            m = tuple(self.SubWordInv(l) for l in m)
        m = self.Add(m, self.roundkeys[:4])
        return bytes(itertools.chain.from_iterable(m))

    @instance_method_cache
    def Add(self, x1, x2):
        try:
            return tuple(self.Add(i, j) for i, j in zip(x1, x2))
        except TypeError:
            return (x1 ^ x2) & 0xFF

    @instance_method_cache
    def Double(self, x):
        return self.Add(x << 1, 0x11B >> (0x80 ^ x & 0x80))

    @instance_method_cache
    def Multiply(self, a, b):
        try:
            return tuple(self.Multiply(i, j) for i, j in zip(a, b))
        except:
            r = 0
            while a:
                r = self.Add(r, b >> ((~a & 1) << 3))
                b = self.Double(b)
                a >>= 1
            return r

    @instance_method_cache
    def RotWord(self, l):
        return l[1:] + l[:1]

    @instance_method_cache
    def RotWordInv(self, l):
        return l[-1:] + l[:-1]

    @instance_method_cache
    def SubWord(self, l):
        return tuple(self.sbox[i] for i in l)

    @instance_method_cache
    def SubWordInv(self, l):
        return tuple(self.sboxinv[i] for i in l)

    @instance_method_cache
    def ShiftRows(self, m):
        return (
            (m[0][0], m[1][1], m[2][2], m[3][3]),
            (m[1][0], m[2][1], m[3][2], m[0][3]),
            (m[2][0], m[3][1], m[0][2], m[1][3]),
            (m[3][0], m[0][1], m[1][2], m[2][3]),
        )

    @instance_method_cache
    def ShiftRowsInv(self, m):
        return (
            (m[0][0], m[3][1], m[2][2], m[1][3]),
            (m[1][0], m[0][1], m[3][2], m[2][3]),
            (m[2][0], m[1][1], m[0][2], m[3][3]),
            (m[3][0], m[2][1], m[1][2], m[0][3]),
        )

    @instance_method_cache
    def MixColumns(self, m):
        return tuple(
            tuple(
                self.Add(
                    self.Add(self.Multiply(2, m[i][j % 4]), m[i][(j + 3) % 4]),
                    self.Add(m[i][(j + 2) % 4], self.Multiply(3, m[i][(j + 1) % 4])),
                )
                for j in range(4)
            )
            for i in range(4)
        )

    @instance_method_cache
    def MixColumnsInv(self, m):
        return tuple(
            tuple(
                self.Add(
                    self.Add(
                        self.Multiply(14, m[i][j % 4]),
                        self.Multiply(9, m[i][(j + 3) % 4]),
                    ),
                    self.Add(
                        self.Multiply(13, m[i][(j + 2) % 4]),
                        self.Multiply(11, m[i][(j + 1) % 4]),
                    ),
                )
                for j in range(4)
            )
            for i in range(4)
        )


from os import urandom
from flask import Flask, request, render_template, jsonify
import logging

log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)
app = Flask(__name__)
flag = tuple(open("flag", "rb").read())
if len(flag) % 16 != 0:
    flag = flag + (0,) * (16 - (len(flag) % 16))
key = open("key", "rb").read()
assert len(key) == 32
cipher = Rijndael(key)
flagenc = cipher.encrypt(flag).hex()


@app.route("/")
def home():
    return render_template("index.html", flagenc=flagenc)


@app.route("/api/enc", methods=["POST"])
def encrypt():
    m = tuple(request.json["a"])
    if len(m) % 16 != 0:
        m = m + (0,) * (16 - (len(m) % 16))
    if request.json["secret"] not in ["secret128", "secret192", "secret256"]:
        k = tuple(request.json["k"])
    else:
        k = key[
            : {"secret128": 16, "secret192": 24, "secret256": 32}[
                request.json["secret"]
            ]
        ]
    try:
        cipher = Rijndael(k)
    except ValueError:
        return jsonify({"result": "Invalid key", "time": 0})
    start = timer()
    enc = cipher.encrypt(m)
    end = timer()
    del cipher
    return jsonify({"result": enc.hex(), "time": end - start})


@app.route("/api/dec", methods=["POST"])
def decrypt():
    m = tuple(request.json["a"])
    if len(m) % 16 != 0:
        m = m + (0,) * (16 - (len(m) % 16))
    if request.json["secret"] not in ["secret128", "secret192", "secret256"]:
        k = tuple(request.json["k"])
    else:
        k = key[
            : {"secret128": 32, "secret192": 48, "secret256": 64}[
                request.json["secret"]
            ]
        ]
    try:
        cipher = Rijndael(k)
    except ValueError:
        return jsonify({"result": "Invalid key", "time": 0})
    start = timer()
    enc = cipher.decrypt(m)
    end = timer()
    del cipher
    for i in range(0, len(flag), 16):
        if flag[i : i + 16] in enc:
            enc = enc.replace(flag[i : i + 16], b"")
    return jsonify({"result": enc.hex(), "time": end - start})


app.run("0.0.0.0", 5000)
