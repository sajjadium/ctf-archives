from Crypto.Util.number import bytes_to_long, long_to_bytes
from secret_process import create_table, laststep
from key import KEY

FLAG = b'IJCTF{' + KEY + b'}'

def int_to_nibble(val):
    sol = []
    for i in range(16):
        sol.append((val >> (4*i)) & 0x0f)
    return sol

def nibble_to_int(val_lst):
    sol = 0
    for i in range(16):
        sol += (val_lst[i] << (4*i))
    return sol

def xor_block(st1, st2):
    output = []
    for i in range(16):
        output.append(st1[i]^st2[i])
    return output

def table_process(st, Ti):
    output = [0] * 16
    for i in range(16):
        output = xor_block(output, Ti[i][st[i]])
    return output

def encrypt(pt, T):
    st = int_to_nibble(bytes_to_long(pt))
    for i in range(1, 31+1):
        st = table_process(st, T[i-1])
    st = table_process(st, T[32-1])
    st = laststep(st)
    st = long_to_bytes(nibble_to_int(st))
    return st

key0T = create_table(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')
print(encrypt(b'TESTCODE', key0T))

keyT = create_table(KEY)
print('table=' + str(keyT))
