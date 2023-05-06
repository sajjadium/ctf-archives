# NOTE!!!!!!!
# This is just a example of secret.py for you to run locally
# The remote implementation is different

import random, sys
import numpy as np
from PIL import Image

# secret key
x0, y0, xp0, yp0 = 0.441, 0.3406, 0.8704, 0.1566
def GenerateNewKey():
    global x0, y0, xp0, yp0
    x0, y0, xp0, yp0 = 0.441, 0.3406, 0.8704, 0.1566

def GenerateNewFlag():
    F = np.asarray(Image.open('example_flag.bmp'))
    return F

def GetSameEntropyImage(F):
    m, n = F.shape
    nrows, ncols = 130, 130
    A = F.reshape(n//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols)
    B = A[::-1,:,:]
    m, n = F.shape
    return B.reshape(n//nrows, -1, nrows, ncols).swapaxes(1,2).reshape(n, m)
    
