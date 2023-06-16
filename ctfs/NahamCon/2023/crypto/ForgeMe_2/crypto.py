import struct
import binascii

""" Implements the SHA1 hash function [1].

    Emulates a barebones version of Python's `hashlib.hash` interface [2],
    providing the simplest parts:
        - update(data): adds binary data to the hash
        - hexdigest(): returns the hexed hash value for the data added thus far

    [1]: https://tools.ietf.org/html/rfc3174.
    [2]: https://docs.python.org/3/library/hashlib.html.
"""

class Sha1:
    def __init__(self, initial:bytes = None):
        self._buffer = b''
        if initial is not None: self.update(initial)

    def update(self, data: bytes):
        if not isinstance(data, bytes):
            raise TypeError(f"expected bytes for data, got {type(data)}")

        self._buffer += data
        return self

    def hexdigest(self, extra_length=0, initial_state=None):
        tag = self.sha1(bytes(self._buffer), extra_length=extra_length, initial_state=initial_state)
        self.clear()
        return tag

    def clear(self):
        self._buffer = b''


    # https://tools.ietf.org/html/rfc3174#section-4
    @staticmethod
    def create_padding(message: bytes, extra_length: int = 0) -> bytes:
        l = (len(message) + extra_length) * 8
        l2 = ((l // 512) + 1) * 512
        padding_length = l2 - l
        if padding_length < 72:
            padding_length += 512
        assert padding_length >= 72, "padding too short"
        assert padding_length % 8 == 0, "padding not multiple of 8"

        # Encode the length and add it to the end of the message.
        zero_bytes = (padding_length - 72) // 8
        length = struct.pack(">Q", l)
        pad = bytes([0x80] + [0] * zero_bytes)

        return pad + length

    @staticmethod
    def pad_message(message: bytes, extra_length: int = 0) -> bytes:
        if not isinstance(message, bytes):
            raise ValueError("expected bytes for message, got %s" % type(message))

        pad = Sha1.create_padding(message, extra_length)
        message = message + pad
        assert (len(message) * 8) % 512 == 0, f"message bitlength ({len(message)}) not a multiple of 512"
        return message

    # https://tools.ietf.org/html/rfc3174#section-6.1
    @staticmethod
    def sha1(message: bytes, initial_state: [int] = None, extra_length: int = 0) -> str:
        """ Returns the 20-byte hex digest of the message.
        >>> Sha1.sha1(b"Hello, world!")
        '943a702d06f34599aee1f8da8ef9f7296031d699'
        """
        H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
        if initial_state is not None:
            if len(initial_state) != 5 or any(not isinstance(x, int) for x in initial_state):
                raise TypeError(f"expected list of 5 ints, got {initial_state}")
            H = initial_state

        # pad according to the RFC (and then some, if specified)
        padded_msg = Sha1.pad_message(message, extra_length=extra_length)

        # break message into chunks
        M = [padded_msg[i:i+64] for i in range(0, len(padded_msg), 64)]
        assert len(M) == len(padded_msg) / 64
        for i in range(len(M)):
            assert len(M[i]) == 64  # sanity check

        # hashing magic
        for i in range(len(M)):
            W = [
                int.from_bytes(M[i][j:j+4], byteorder="big")
                for j in range(0, len(M[i]), 4)
            ]
            assert len(W) == 16
            assert type(W[0]) == int
            assert W[0] == (M[i][0] << 24) + (M[i][1] << 16) + (M[i][2] << 8) + M[i][3]

            for t in range(16, 80):
                W.append(Sha1._S(1, W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16]))

            A, B, C, D, E = H
            for t in range(80):
                TEMP = (((((((Sha1._S(5, A) + Sha1._f(t, B, C, D)) & 0xFFFFFFFF) + E) & 0xFFFFFFFF) + W[t]) & 0xFFFFFFFF) + Sha1._K(t)) & 0xFFFFFFFF
                assert TEMP == (Sha1._S(5, A) + Sha1._f(t, B, C, D) + E + W[t] + Sha1._K(t)) & 0xFFFFFFFF
                E, D, C, B, A = D, C, Sha1._S(30, B), A, TEMP

            H = [
                (H[0] + A) & 0xFFFFFFFF,
                (H[1] + B) & 0xFFFFFFFF,
                (H[2] + C) & 0xFFFFFFFF,
                (H[3] + D) & 0xFFFFFFFF,
                (H[4] + E) & 0xFFFFFFFF,
            ]

        # craft the hex digest
        th = lambda h: hex(h)[2:] # trimmed hex
        return "".join("0" * (8 - len(th(h))) + th(h) for h in H)

    @staticmethod
    def _f(t, B, C, D):
        if t >= 0 and t <= 19:    return ((B & C) | ((~B) & D)) & 0xFFFFFFFF
        elif t >= 20 and t <= 39: return (B ^ C ^ D) & 0xFFFFFFFF
        elif t >= 40 and t <= 59: return ((B & C) | (B & D) | (C & D)) & 0xFFFFFFFF
        elif t >= 60 and t <= 79: return (B ^ C ^ D) & 0xFFFFFFFF
        assert False

    @staticmethod
    def _K(t):
        if t >= 0 and t <= 19:    return 0x5A827999
        elif t >= 20 and t <= 39: return 0x6ED9EBA1
        elif t >= 40 and t <= 59: return 0x8F1BBCDC
        elif t >= 60 and t <= 79: return 0xCA62C1D6
        assert False

    @staticmethod
    def _S(n, X):
        assert n >= 0 and n < 32, "n not in range"
        assert (X >> 32) == 0, "X too large"
        result = ((X << n) | (X >> (32-n))) & 0xFFFFFFFF
        assert (result >> 32) == 0, "result too large"
        return result

