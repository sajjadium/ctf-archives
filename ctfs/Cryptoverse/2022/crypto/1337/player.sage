from Crypto.Util.number import inverse, bytes_to_long, getPrime

FLAG = b"cvctf{REDACTED}"
step = len(FLAG) // 4
parts = []
for i in range(0, len(FLAG), step):
    parts.append(bytes_to_long(FLAG[i:i+step]))

P = getPrime(128)
ZmodP = Zmod(P)
a, b, c, d = parts
x, y, z, w = ZmodP(a), ZmodP(b), ZmodP(c), ZmodP(d)

print("P:", P)
print("L:", x^1+y^3+z^3+w^7)
print("E:", y^1+z^3+w^3+x^7)
print("E:", z^1+w^3+x^3+y^7)
print("E:", w^1+x^3+y^3+z^7)
print("T:", x+y+z+w)

'''
P: 231609284865232306744388160907453774453
L: 213929627434382339098735177055751649916
E: 19199104003461693263250446715340616788
E: 81305572597778258494448971196865605263
E: 204055349607012377951682156574173649079
T: 2268211308285612387872477045295901103
'''