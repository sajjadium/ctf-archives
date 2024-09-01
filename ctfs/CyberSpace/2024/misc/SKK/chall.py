import numpy as np
import cv2
import random
from datetime import datetime

img = cv2.imread('flag.png')
size_x, size_y = img.shape[:2]

enc_negpos = np.zeros_like(img)

random.seed(datetime.now().timestamp())

for i in range(size_x):
    for j in range(size_y):
        for rgb in range(3):
            negpos = random.random()
            if negpos < 0.5:
                enc_negpos[i, j, rgb] = img[i, j, rgb]
            else:
                enc_negpos[i, j, rgb] = img[i, j, rgb] ^ 255


enc_shuffle = enc_negpos.copy()

for i in range(size_x):
    for j in range(size_y):
        shuffle = random.randint(1, 6)
        if shuffle == 1:
            enc_shuffle[i, j] = enc_negpos[i, j]
        elif shuffle == 2:
            enc_shuffle[i, j] = enc_negpos[i, j][[0, 2, 1]]
        elif shuffle == 3:
            enc_shuffle[i, j] = enc_negpos[i, j][[1, 0, 2]]
        elif shuffle == 4:
            enc_shuffle[i, j] = enc_negpos[i, j][[1, 2, 0]]
        elif shuffle == 5:
            enc_shuffle[i, j] = enc_negpos[i, j][[2, 0, 1]]
        else:
            enc_shuffle[i, j] = enc_negpos[i, j][[2, 1, 0]]


cv2.imwrite('enc.png', enc_shuffle)