#!/usr/bin/env python3
# pip install matplotlib
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = []
ys = []
zs = []
cs = []

for line in sys.stdin.readlines():
    print(line.strip())
    if line.startswith(' > '):
        continue
    x, y, z, c = map(lambda x: int(x.strip()), line.split(' '))
    xs.append(x)
    ys.append(y)
    zs.append(z)
    cs.append(c)

ax.set_ylim(0, 250)
ax.set_xlim(0, 250)
ax.set_zlim(0, 250)

img = ax.scatter(xs, ys, zs, c=cs, cmap=plt.hot())
fig.colorbar(img)
plt.show()
