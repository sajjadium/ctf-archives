#!/usr/bin/env python3

import ctypes


dilithium_lib = ctypes.CDLL('./libpqcrystals_dilithium2_ref.so')
def verify(sm, pk):
    if len(sm) < 1268:
        return False
    msg_buf = ctypes.c_buffer(len(sm))
    msg_len = ctypes.c_size_t()
    sm_buf = ctypes.c_buffer(sm)
    pk_buf = ctypes.c_buffer(pk)
    verified = dilithium_lib.pqcrystals_dilithium2_ref_open(msg_buf, ctypes.byref(msg_len), sm_buf, len(sm), pk_buf)
    if verified != 0:
        return False
    return bytes(msg_buf)[:msg_len.value]


def main():
    TARGET = b'dilithium crystals'
    pk_bytes = open('pk.bin', 'rb').read()
    print('pk:', pk_bytes.hex())

    sm = bytes.fromhex(input('signed message (hex): '))
    msg = verify(sm, pk_bytes)
    if msg is False:
        print('Invalid signature!')
    else:
        print('Signature verified for message', msg)
        if msg == TARGET:
            FLAG = open('flag.txt', 'r').read().strip()
            print(FLAG)


if __name__ == '__main__':
    main()
