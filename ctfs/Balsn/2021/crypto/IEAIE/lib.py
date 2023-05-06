import math
import functools
import numpy as np
from scipy.stats import entropy
from skimage.measure import shannon_entropy
from secret import x0, y0, xp0, yp0, GenerateNewKey, GenerateNewFlag, GetSameEntropyImage

mu = 0.8116

@functools.lru_cache(maxsize=None)
def LASM2D(mu, x0, y0, ret_num, skip_num=200):
    iter_num = ret_num//2+ret_num%2
    xi = x0
    yi = y0
    ret_seq = []
    for i in range(skip_num+iter_num):
        xi = math.sin(math.pi*mu*(yi+3)*xi*(1-xi))
        yi = math.sin(math.pi*mu*(xi+3)*yi*(1-yi))
        if i >= skip_num:
            ret_seq.append(xi)
            ret_seq.append(yi)
    ret_seq = ret_seq[:ret_num]
    return np.array(ret_seq)

def Entropy(img):
    # grayscale
    v,c = np.unique(img, return_counts=True)
    counts = np.zeros(256, dtype=int)
    counts[v] = c
    return entropy(counts, base=2)

def UpdateKey1(x0, y0, xp0, yp0, s):
    x_bar0 = (x0+(s+1)/(s+xp0+yp0+1))%1
    y_bar0 = (y0+(s+2)/(s+xp0+yp0+2))%1
    return x_bar0, y_bar0

def UpdateKey2(x0, y0, xp0, yp0):
    xp_bar0 = (xp0+(1/(x0+y0+1)))%1
    yp_bar0 = (yp0+(2/(x0+y0+2)))%1
    return xp_bar0, yp_bar0

def Uniq(seq):
    now_set = set()
    min_num = 0
    for i, s in enumerate(seq):
        if s not in now_set:
            now_set.add(s)
            if s == min_num:
                while min_num in now_set:
                    min_num += 1
        else:
            seq[i] = min_num
            now_set.add(min_num)
            while min_num in now_set:
                min_num += 1

