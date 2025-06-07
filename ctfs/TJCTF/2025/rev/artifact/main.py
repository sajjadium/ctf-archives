import sys
from time import perf_counter
from math import pi,sqrt,asin,degrees,radians,sin

circ = 24901
diam = (circ / (2 * pi)) ** 2 
rad = sqrt(diam)
spin = 1000

def add_spin(points,time):
    ang = time / circ * 360
    for i in range(len(points)):
        nang = find_ang(points[i]) + ang
        points[i] = sin(radians(nang)) * rad

def find_ang(point):
    return degrees(asin(point / rad))

flag = b'tjctf{fake_flag}'
points = []
base = []
for i in flag:
    base.append(sqrt(diam - (i * 31) ** 2))
    st=perf_counter()
    points.append(sqrt(diam - (i * 31) ** 2))
    u = 0
    while u < 1000000:
        u += 1
    en = perf_counter()
    time = (en - st) * spin
    print(int(time))
    add_spin(points,time)

with open("points.txt",'w') as w:
    w.write(str(points))
