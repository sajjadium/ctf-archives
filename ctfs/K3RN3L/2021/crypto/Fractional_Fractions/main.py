from Crypto.Util.number import bytes_to_long
flag = str(bytes_to_long(open('flag.txt','rb').read()))
from fractions import Fraction
enc = Fraction(0/1)
for c in flag:
    enc += Fraction(int(c)+1)
    enc = 1/enc
print(enc)
#7817806454609461952471483475242846271662326/63314799458349217804506955537187514185318043
