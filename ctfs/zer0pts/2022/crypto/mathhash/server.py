import struct
import math
import signal
import os

def MathHash(m):
    hashval = 0
    for i in range(len(m)-7):
        c = struct.unpack('<Q', m[i:i+8])[0]
        t = math.tan(c * math.pi / (1<<64))
        hashval ^= struct.unpack('<Q', struct.pack('<d', t))[0]
    return hashval

if __name__ == '__main__':
    FLAG = os.getenv('FLAG', 'zer0pts<sample_flag>').encode()
    assert FLAG.startswith(b'zer0pts')

    signal.alarm(1800)
    try:
        while True:
            key = bytes.fromhex(input("Key: "))
            assert len(FLAG) >= len(key)

            flag = FLAG
            for i, c in enumerate(key):
                flag = flag[:i] + bytes([(flag[i] + key[i]) % 0x100]) + flag[i+1:]

            h = MathHash(flag)
            print("Hash: " + hex(h))
    except:
        exit(0)
