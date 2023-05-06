import numpy as np
from scipy import ndimage
from PIL import Image

i = Image.open("flag.png")
a = np.array(i)
a = np.transpose(a,(2,0,1))
r = a[0]
g = a[1]
b = a[2]
k = np.array([[0,0,0],[0,0.25,0.25],[0,0.25,0.25]])
r2 = ndimage.convolve(r,k,mode="constant",cval=0)
g2 = ndimage.convolve(g,k,mode="constant",cval=0)
b2 = ndimage.convolve(b,k,mode="constant",cval=0)
out = Image.fromarray(np.transpose(np.array([r2,g2,b2]),(1,2,0)))
out.save("chall.png")