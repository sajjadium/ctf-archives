from secrets import randbits
from Crypto.Util.number import bytes_to_long

# get a one-time-pad in which exactly half the bits are set
def get_xorpad(bitlength):
    xorpad = randbits(bitlength)
    return xorpad if bin(xorpad).count('1') == bitlength // 2 else get_xorpad(bitlength)

def leak_encrypted_flag():
    from secret import flag
    return bytes_to_long(flag.encode()) ^ get_xorpad(len(flag) * 8)

# I managed to leak the encrypted flag a few times
if __name__ == '__main__':
    for _ in range(200):
        print(leak_encrypted_flag())
