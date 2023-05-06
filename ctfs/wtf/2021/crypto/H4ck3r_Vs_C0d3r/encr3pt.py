from PIL import Image, ImageDraw
import os
import sys
from random import SystemRandom
random = SystemRandom()
xrange = range


I3 = Image.open

if len(sys.argv) != 2:
    exit()

fl = str(sys.argv[1])

O1 = os.path.isfile
O2 = os.path.splitext

if not O1(fl):
    exit()

i = I3(fl)

f, e = O2(fl)
O_A = f+"_A.png"
O_B = f+"_B.png"

i = i.convert('1')

I1 = Image.new
I2 = ImageDraw.Draw

a = i.size[0]*2
b = i.size[1]*2
i_A = I1('1', (a, b))
d_A = I2(i_A)
i_B = I1('1', (a, b))
d_B = I2(i_B)


ps = ((1, 1, 0, 0), (1, 0, 1, 0), (1, 0, 0, 1),
      (0, 1, 1, 0), (0, 1, 0, 1), (0, 0, 1, 1))

for x in xrange(0, int(a/2)):
    for y in xrange(0, int(b/2)):
        pix = i.getpixel((x, y))
        p = random.choice(ps)
        d_A.point((x*2, y*2), p[0])
        d_A.point((x*2+1, y*2), p[1])
        d_A.point((x*2, y*2+1), p[2])
        d_A.point((x*2+1, y*2+1), p[3])
        if pix == 0:
            d_B.point((x*2, y*2), 1-p[0])
            d_B.point((x*2+1, y*2), 1-p[1])
            d_B.point((x*2, y*2+1), 1-p[2])
            d_B.point((x*2+1, y*2+1), 1-p[3])
        else:
            d_B.point((x*2, y*2), p[0])
            d_B.point((x*2+1, y*2), p[1])
            d_B.point((x*2, y*2+1), p[2])
            d_B.point((x*2+1, y*2+1), p[3])

i_A.save(O_A, 'PNG')
i_B.save(O_B, 'PNG')
