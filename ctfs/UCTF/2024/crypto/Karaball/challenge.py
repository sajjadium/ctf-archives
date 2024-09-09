from ECC import Curve, Coord
from secrets import randbelow

flag = "uctf{test_flag}"
signatures = {}
valid_hosts = {'uctf.ir'}

a = 0x0
b = 0x7
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

ecc = Curve(a, b, p)
G = Coord(Gx, Gy)

assert ecc.is_on_curve(G)


for host in valid_hosts:
    d = randbelow(p)
    Q = ecc.sign(G, d)
    signatures[host] = [hex(Q.x),hex(Q.y)]
    
print(signatures)
print("Give me your generator and private key for verification process")

data0 = input("G(x,y) in hex format: ")
data1 = input("d in hex format: ")

try:
    Coordinates = data0.split(',')
    PrivateKey = data1
    G1 = Coord(int(Coordinates[0], 16), int(Coordinates[1], 16))
    d1 = int(PrivateKey, 16)
except Exception as e:
    print('Wrong format! try again.')
    exit()


if not ecc.is_on_curve(G1):
    print('Point is not on the curve!')
    exit()

if d1 < 2:
    print("Security Issues Discovered!")
    exit()

sig = ecc.sign(G1, d1)

if sig.x == int(signatures['uctf.ir'][0], 16) and sig.y == int(signatures['uctf.ir'][1], 16):
    print(f"Access granted. Here is your reward : {flag}".encode())
else:
    print("Verficication process failed!")