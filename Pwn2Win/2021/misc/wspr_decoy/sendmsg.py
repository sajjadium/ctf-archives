#!/usr/bin/env python3
from modulator import modulator
from hashlib import sha3_224
from datetime import datetime
import re
import time
import string


class WSPR:
    """ https://github.com/brainwagon/genwspr """
    syncv = [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0,
             1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0,
             0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1,
             0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1,
             0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0,
             0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0,
             0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0]

    @staticmethod
    def normalizecallsign(callsign):
        callsign = list(callsign)
        idx = None
        for i, ch in enumerate(callsign):
            if ch in string.digits:
                idx = i
        assert idx is not None
        newcallsign = 6 * [" "]
        newcallsign[2-idx:2-idx+len(callsign)] = callsign
        return ''.join(newcallsign)

    @staticmethod
    def encodecallsign(callsign):
        callsign = WSPR.normalizecallsign(callsign)
        lds = string.digits + string.ascii_uppercase + " "
        ld = string.digits + string.ascii_uppercase
        d = string.digits
        ls = string.ascii_uppercase + " "
        acc = lds.find(callsign[0])
        acc *= len(ld)
        acc += ld.find(callsign[1])
        acc *= len(d)
        acc += d.find(callsign[2])
        acc *= len(ls)
        acc += ls.find(callsign[3])
        acc *= len(ls)
        acc += ls.find(callsign[4])
        acc *= len(ls)
        acc += ls.find(callsign[5])
        return WSPR.tobin(acc, 28)

    @staticmethod
    def tobin(v, l):
        x = []
        while v != 0:
            x.append(str(v % 2))
            v = v // 2
        while len(x) < l:
            x.append("0")
        x.reverse()
        return ''.join(x)[0:l]

    @staticmethod
    def grid2ll(grid):
        if re.match(r'[A-R][A-R][0-9][0-9]([a-x][a-x])?$', grid):
            # go ahead and decode it.
            p = (ord(grid[0])-ord('A'))
            p *= 10
            p += (ord(grid[2])-ord('0'))
            p *= 24
            if len(grid) == 4:
                p += 12
            else:
                p += (ord(grid[4])-ord('a')) + 0.5
            lng = (p / 12) - 180.0
            p = (ord(grid[1])-ord('A'))
            p *= 10
            p += (ord(grid[3])-ord('0'))
            p *= 24
            if len(grid) == 4:
                p += 12
            else:
                p += (ord(grid[5])-ord('a')) + 0.5
            lat = (p / 24) - 90.0
            return (lat, lng)
        else:
            raise ValueError('Malformed grid reference "%s"' % grid)

    @staticmethod
    def encodegrid(grid):
        lat, long = WSPR.grid2ll(grid)
        long = int((180 - long) / 2.0)
        lat = int(lat + 90.)
        return WSPR.tobin(long * 180 + lat, 15)

    @staticmethod
    def encodepower(power):
        assert power in {0, 3, 7, 10, 13, 17, 20, 23,
                         27, 30, 33, 37, 40, 43, 47, 50, 53, 57, 60}
        power = power + 64
        return WSPR.tobin(power, 7)

    class convolver:
        def __init__(self):
            self.acc = 0

        def encode(self, bit):
            self.acc = ((self.acc << 1) & 0xFFFFFFFF) | bit
            return WSPR.parity(self.acc & 0xf2d05351), WSPR.parity(self.acc & 0xe4613c47)

    @staticmethod
    def encode(l):
        e = WSPR.convolver()
        f = []
        l = map(lambda x: int(x), list(l))
        for x in l:
            b0, b1 = e.encode(x)
            f.append(b0)
            f.append(b1)
        return f

    @staticmethod
    def parity(x):
        even = 0
        while x:
            even = 1 - even
            x = x & (x - 1)
        return even

    @staticmethod
    def bitstring(x):
        return ''.join([str((x >> i) & 1) for i in (7, 6, 5, 4, 3, 2, 1, 0)])

    @staticmethod
    def bitreverse(x):
        bs = WSPR.bitstring(x)
        return int(bs[::-1], 2)

    @staticmethod
    def produce_symbols(callsign, grid, power):
        idx = range(0, 256)
        ridx = list(filter(lambda x: x < 162, map(
            lambda x: WSPR.bitreverse(x), idx)))

        callsign = WSPR.encodecallsign(callsign)
        grid = WSPR.encodegrid(grid)
        power = WSPR.encodepower(power)

        message = callsign + grid + power + 31 * '0'
        message = WSPR.encode(message)

        # interleave...
        imessage = 162 * [0]

        for x in range(162):
            imessage[ridx[x]] = message[x]

        return [(2*x+y) for x, y in zip(imessage, WSPR.syncv)]


class SpinalEncoder:
    """ http://nms.csail.mit.edu/papers/fp049-perry.pdf """

    @staticmethod
    def h(s_i, m_i):
        return sha3_224(s_i + m_i).digest()

    @staticmethod
    def rng(s_i, seed, nbits):
        assert nbits <= 8
        # our variant of the algorithm uses an additional seed so that different
        # frames containing the same data result in different symbols
        bits = bin(sha3_224(s_i + seed).digest()[-1])[2:].rjust(8, '0')
        return bits[8-nbits:]

    @staticmethod
    def encode(seed, M, size, k=4):
        # generate spine values
        s_i = b''
        spine = []
        for i in range(0, len(M), k):
            m_i = bytes([int('0b' + M[i:i+k], 2)])
            s_i = SpinalEncoder.h(s_i, m_i)
            spine.append(s_i)
        symbols = []
        # generate symbols
        rng_bits = size // len(spine)
        for i, s_i in enumerate(spine):
            b = rng_bits
            if i == len(spine) - 1:
                # use additional bits for the last spine value
                b += size % len(spine)
            symbols.append(SpinalEncoder.rng(s_i, seed, b))
        # interleave symbols
        res = []
        for i in range(rng_bits):
            for symbol in symbols:
                res.append(symbol[i])
        res.extend(symbols[-1][rng_bits:])
        return ','.join(res)


def string_to_bits(s):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ{}-_?!'
    bits_per_char = 5
    assert 1 << bits_per_char == len(alphabet)
    bits = ''
    for c in s:
        bits += WSPR.tobin(alphabet.index(c), bits_per_char)
    return bits


def random_freq(seed):
    r = sha3_224(seed).digest()[0]/255
    return int(7040000 + (200-6-23)*r)


def main():
    at_min = 0
    callsign = 'PU2UID'
    grid = 'GG68'
    power = 37
    with open('flag.txt') as f:
        flag = string_to_bits(f.read().strip())

    assert at_min % 2 == 0
    assert len(flag) == 5*32

    next_timestamp = 60*at_min + 600*((time.time() + 600) // 600)

    seed = sha3_224(b'%d' % next_timestamp).digest()

    freq = random_freq(seed)
    wspr_symbols = WSPR.produce_symbols(callsign, grid, power)
    am_symbols = SpinalEncoder.encode(seed, flag, len(wspr_symbols))
    wspr_symbols = ','.join(str(x) for x in wspr_symbols)

    print('PRNG seed = {}'.format(seed.hex()))
    print('Waiting until {} to TX at {} Hz'.format(
        datetime.fromtimestamp(next_timestamp).strftime('%Y-%m-%d %H:%M:%S'),
        freq))

    m = modulator(
        freq=freq,
        wspr_symbols=wspr_symbols,
        am_symbols=am_symbols,
    )

    time.sleep(next_timestamp - time.time())
    m.start()
    m.wait()


if __name__ == '__main__':
    main()
