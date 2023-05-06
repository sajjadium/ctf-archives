#!/usr/bin/env python3
import ctypes

MAX_QUERIES = 7681
FLAG = open('flag.txt', 'rb').read().strip()


kyber_lib = ctypes.CDLL('./libpqcrystals_kyber512_ref.so')
class Kyber:
    def __init__(self):
        self.pk_buf = ctypes.c_buffer(800)
        self.sk_buf = ctypes.c_buffer(1632)
        kyber_lib.pqcrystals_kyber512_ref_keypair(self.pk_buf, self.sk_buf)

    def kem_enc(self):
        ct_buf = ctypes.c_buffer(1024)
        ss_buf = ctypes.c_buffer(32)
        kyber_lib.pqcrystals_kyber512_ref_enc(ct_buf, ss_buf, self.pk_buf)
        return bytes(ct_buf), bytes(ss_buf)

    def kem_dec(self, c):
        assert len(c) == 1024
        ct_buf = ctypes.c_buffer(c)
        ss_buf = ctypes.c_buffer(32)
        kyber_lib.pqcrystals_kyber512_ref_dec(ss_buf, ct_buf, self.sk_buf)
        return bytes(ss_buf)


def main():
    kyber = Kyber()
    print('pk:', bytes(kyber.pk_buf).hex())
    print('H(pk):', bytes(kyber.sk_buf)[-64:].hex())

    for _ in range(MAX_QUERIES):
        try:
            inp = input('> ')
            if inp.startswith('enc'):
                ct, ss = kyber.kem_enc()
                print('ct:', ct.hex())
                print('ss:', ss.hex())
            elif inp.startswith('dec '):
                ct = bytes.fromhex(inp[4:])
                ss = kyber.kem_dec(ct)
                print('ss:', ss.hex())
            else:
                break
        except:
            print('>:(')
            exit(1)

    enc = bytes([a ^ b for a, b in zip(FLAG, bytes(kyber.sk_buf))])
    print('flag_enc:', enc.hex())


if __name__ == '__main__':
    main()
