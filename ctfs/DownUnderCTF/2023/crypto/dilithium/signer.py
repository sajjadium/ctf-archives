import ctypes
import random


dilithium_lib = ctypes.CDLL('./libpqcrystals_dilithium2_ref.so')
def sign(msg, sk_buf):
    sm_buf = ctypes.c_buffer(1268 + len(msg))
    msg_buf = ctypes.c_buffer(msg)
    sm_len = ctypes.pointer(ctypes.c_size_t())
    dilithium_lib.pqcrystals_dilithium2_ref(sm_buf, sm_len, msg_buf, len(msg), sk_buf)
    return bytes(sm_buf)


def main():
    sk_buf = ctypes.c_buffer(2336)
    pk_buf = ctypes.c_buffer(1312)
    dilithium_lib.pqcrystals_dilithium2_ref_keypair(pk_buf, sk_buf)
    open('pk.bin', 'wb').write(bytes(pk_buf))

    with open('signatures.dat', 'wb') as f:
        for _ in range(19091):
            sig = sign(random.randbytes(4), sk_buf)
            f.write(sig)


if __name__ == '__main__':
    main()
