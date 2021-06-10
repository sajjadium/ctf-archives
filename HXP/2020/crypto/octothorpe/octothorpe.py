#!/usr/bin/env python3

import math

class octothorpe:
    digest_size = 16
    block_size = 64
    name = "octothorpe"

    state_size = 16
    shift_count = 64
    round_count = 20
    initial_state = bytearray.fromhex('00112233445566778899aabbccddeeff')

    function = lambda i: math.cos(i ** 3)
    sbox = sorted(range(256), key=function)
    shift = [int(8 * s) % 8 for s in map(function, range(shift_count))]

    new = classmethod(lambda cls, data: cls(data))
    copy = lambda self: octothorpe(_cache=self._cache[:], _length=self._length, _state=self._state[:])
    digest = lambda self: bytes(self._finalize())
    hexdigest = lambda self: self.digest().hex()

    def __init__(self, data: bytes = None, *, _cache: bytes = None, _length: int = None, _state: bytearray = None) -> None:
        self._cache = _cache or b''
        self._length = _length or 0
        self._state = _state or self.initial_state[:]
        assert len(self._state) == self.state_size, 'Invalid state size'
        if data:
            self.update(data)

    def update(self, data: bytes) -> None:
        self._cache += data
        while len(self._cache) >= self.block_size:
            block, self._cache = self._cache[:self.block_size], self._cache[self.block_size:]
            self._compress(block)
            self._length += self.block_size

    def _finalize(self) -> bytearray:
        clone = self.copy()
        clone._length += len(clone._cache)
        clone.update(b'\x80' + b'\x00' * ((self.block_size - 9 - clone._length) % self.block_size) + (8 * clone._length).to_bytes(8, 'little'))
        return clone._state

    def _compress(self, block: bytes) -> None:
        prev_state = lambda index: (index - 1) % self.state_size
        next_state = lambda index: (index + 1) % self.state_size
        rol = lambda value, shift, size: ((value << (shift % size)) | (value >> (size - (shift % size)))) & ((1 << size) - 1)
        ror = lambda value, shift, size: ((value >> (shift % size)) | (value << (size - (shift % size)))) & ((1 << size) - 1)
        for r in range(self.round_count):
            state = self._state[:]
            for i in range(self.block_size):
                j, jj = (i * r) % self.state_size, (i * r) % self.shift_count
                self._state[prev_state(j)] ^= self.sbox[block[i] ^ rol(state[j], self.shift[jj], 8)]
                self._state[next_state(j)] ^= self.sbox[block[i] ^ ror(state[j], self.shift[jj], 8)]

if __name__ == '__main__':
    assert octothorpe(b'hxp').hexdigest() == '4e072c7a1872f7cdf3cb2cfc676b0311'
