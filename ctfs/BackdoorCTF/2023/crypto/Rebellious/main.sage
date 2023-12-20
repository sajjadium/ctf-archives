from sage.all import *
from Crypto.Util.number import *
import random
import time
random.seed(time.time())


FLAG = b'flag{REDACTED}' ## flag removed
flag = bytes_to_long(FLAG)

f = open('./output.txt', 'w')

p = 2653051169113192956861029164111253541045934291082610203810454254019428617095444726883436858598608538656059147405437762506043477080240989129049112094108099635297397071457202368492446105766960803000479292350528610656494430695078098921185726745996662867511185527654339397
F = GF(p)

a, b = random.randint(2, p), random.randint(2, p)
f.write(f"a = {a}\nb = {b}")

def point_addition(px, py, qx, qy):
    rx = F((pow(a, -1, p) * (px * qx - py * qy * (a ** 2) * (pow(b ** 2, - 1, p)))) % p)
    ry = F((pow(a, -1, p) * (px * qy + py * qx)) % p)
    return (rx, ry)

def scalar_multiplication(px, py, k):
    rx = a
    ry = 0
    while k:
        if k % 2:
            rx, ry = point_addition(rx, ry, px, py)
        px, py = point_addition(px, py, px, py)
        k >>= 1
    return rx, ry

G = generator_curve() ## implementation hidden for enhancing security

x1 = G[0]
y1 = G[1]

H = scalar(multiplication(x1, y1, flag))

x2 = H[0]
y2 = H[1]

f.write(f"x1 = {x1}\n")
f.write(f"y1 = {y1}\n")
f.write(f"x2 = {x2}\n")
f.write(f"y2 = {y2}\n")

