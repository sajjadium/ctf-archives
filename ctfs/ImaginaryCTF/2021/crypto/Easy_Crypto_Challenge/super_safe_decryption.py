from sage.all import *

# read encrypted
Cs = open("out.txt", "r").readlines()

# initialize same curve
p = 692893
a = 1
b = 6
E = EllipticCurve(GF(p),[a,b])

# initialize Bob's decryption
P = E(683798, 652629)
kA = 4001
#!!!0hH no0... tH3 F1le g07 corRuPt3D!!!#56
B = #!!!0hH no0... tH3 F1le g07 corRuPt3D!!!#* P

# convert encrypted to points on the curve
Cs = [C.split(":") for C in Cs]
Cs = [E(C[0][1:-1], C[1][1:-1]) for C in Cs]

# now decrypt those points
plain = ""
for C in Cs:
	M = #!!!0hH no0... tH3 F1le g07 corRuPt3D!!!#
	x = M[0]
	plain += #!!!0hH no0... tH3 F1le g07 corRuPt3D!!!# >> 5)

print(plain)