#!/usr/bin/env python3
import sys
import random
import base64
import struct

KEY_LEN = 16
TAG_LEN = 16

def generate_key():
    return random.randbytes(KEY_LEN)

def import_key(path):
    key = base64.b64decode(open(path, 'rb').read().strip())
    assert len(key) == KEY_LEN
    return key

def export_key(key, path):
    open(path, 'wb').write(base64.b64encode(key) + b'\n')

def xor(s, t):
    return bytes(x ^ y for x, y in zip(s, t))

def enc(k, b, n=32):
    v0, v1 = struct.unpack('!2I', b)
    s, d, m = 0, 0x9e3779b9, 0xffffffff
    for _ in range(n):
        v0 = (v0 + (((v1 << 4 ^ v1 >> 5) + v1) ^ (s + k[s & 3]))) & m
        s = (s + d) & m
        v1 = (v1 +
              (((v0 << 4 ^ v0 >> 5) + v0) ^ (s + k[s >> 11 & 3]))) & m
    return struct.pack('!2I', v0, v1)

def mac(key, buf, iv=None):
    buf += b'\0' * (8 - len(buf) % 8)
    k = struct.unpack('!4I', key)
    iv = iv or random.randbytes(8)
    c = iv
    for i in range(0, len(buf), 8):
        p = buf[i : i + 8]
        c = enc(k, xor(p, c))
    tag = iv + c
    assert len(tag) == TAG_LEN
    return tag

def sign(key, buf):
    tag = mac(key, buf)
    return \
        b'-----BEGIN MAC-----\n' + \
        base64.b64encode(tag) + b'\n' \
        b'-----END MAC-----\n' + \
        buf

def verify(key, buf):
    line, buf = buf.split(b'\n', 1)
    assert line == b'-----BEGIN MAC-----'
    b64tag, buf = buf.split(b'\n', 1)
    tag = base64.b64decode(b64tag)
    line, buf = buf.split(b'\n', 1)
    assert line == b'-----END MAC-----'

    tag2 = mac(key, buf, tag[:8])
    if tag == tag2:
        return buf

if __name__ == '__main__':
    def usage():
        print(
            f'usage: {sys.argv[0]} genkey [--seed SEED] KEYFILE\n'
            f'   OR  {sys.argv[0]} sign [--seed SEED] KEYFILE < FILE > FILE\n'
            f'   OR  {sys.argv[0]} verify KEYFILE < FILE',
            file=sys.stderr
        )
        exit(1)

    if '--seed' in sys.argv:
        i = sys.argv.index('--seed')
        try:
            seed = int(sys.argv[i + 1])
        except:
            usage()
        random.seed(seed)
        sys.argv[i : i + 2] = []

    argc = len(sys.argv)
    if argc != 3:
        usage()

    cmd = sys.argv[1]
    keyfile = sys.argv[2]

    if cmd == 'genkey':
        key = generate_key()
        export_key(key, keyfile)

    elif cmd in ('sign', 'verify'):
        key = import_key(keyfile)
        if cmd == 'sign':
            sys.stdout.buffer.write(sign(key, sys.stdin.buffer.read()))
        else:
            if verify(key, sys.stdin.buffer.read()):
                exit(0)
            else:
                exit(1)

    else:
        usage()
