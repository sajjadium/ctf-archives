#!/usr/bin/env python3

import ctypes, os, signal
import hashlib


MAX_QUERIES = 56
FLAG = os.getenv('FLAG', 'DUCTF{testflag}').encode()


kyber_lib = ctypes.CDLL('./libpqcrystals_kyber512_ref.so')
class Kyber:
    def __init__(self):
        self.pk_buf = ctypes.c_buffer(800)
        self.sk_buf = ctypes.c_buffer(768)
        kyber_lib.pqcrystals_kyber512_ref_indcpa_keypair(self.pk_buf, self.sk_buf)

    def encrypt(self, m):
        assert len(m) == 32
        ct_buf = ctypes.c_buffer(768)
        m_buf = ctypes.c_buffer(m)
        r = ctypes.c_buffer(os.urandom(32))
        kyber_lib.pqcrystals_kyber512_ref_indcpa_enc(ct_buf, m_buf, self.pk_buf, r)
        return bytes(ct_buf)

    def decrypt(self, c):
        assert len(c) == 768
        ct_buf = ctypes.c_buffer(c)
        m_buf = ctypes.c_buffer(32)
        kyber_lib.pqcrystals_kyber512_ref_indcpa_dec(m_buf, ct_buf, self.sk_buf)
        return bytes(m_buf)


def main():
    kyber = Kyber()
    print('pk:', bytes(kyber.pk_buf).hex())

    assert kyber.decrypt(kyber.encrypt(b'x'*32)) == b'x'*32

    for _ in range(MAX_QUERIES):
        try:
            inp = input('> ')
            c = bytes.fromhex(inp)
            m = kyber.decrypt(c)
            print(hashlib.sha256(m).hexdigest())
        except:
            print('>:(')
            exit(1)

    k = hashlib.sha512(bytes(kyber.sk_buf)).digest()
    enc = bytes([a ^ b for a, b in zip(FLAG, k)])
    print('flag_enc:', enc.hex())


if __name__ == '__main__':
    signal.alarm(100)
    main()
