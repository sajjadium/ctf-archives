from mpmath import mp, power, ln
import json

mp.dps = 1000000000

def decode(enc):
    return int(power(2, enc * ln(2)))

s, e = json.load(open('encoded.json'))
flag = decode(s << e)

print(flag.to_bytes((flag.bit_length() + 7) // 8, 'big')[:74])
