from secrets import randbits
from Crypto.Util.number import bytes_to_long
import os

flag = os.environ.get('FLAG', 'SEE{not_the_real_flag}').encode()

# get a one-time-pad in which not exactly half the bits are set
def get_xorpad(bitlength):
    xorpad = randbits(bitlength)
    return xorpad if bin(xorpad).count('1') != bitlength // 2 else get_xorpad(bitlength)

def leak_encrypted_flag():
    return bytes_to_long(flag) ^ get_xorpad(len(flag) * 8)

# I managed to leak the encrypted flag a lot of times
if __name__ == '__main__':
    for _ in range(2**16):
        print(leak_encrypted_flag())