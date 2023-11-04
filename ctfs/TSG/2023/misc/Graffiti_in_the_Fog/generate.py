import numpy as np
import cv2
from scipy.stats import ortho_group

DIM = 4

def shuffle(data, vecR):
    length = len(data)
    perturbation = (np.random.rand(length, 1) - 0.5) * 500.0
    return data + perturbation * vecR

if __name__ == "__main__":
    img = cv2.imread("flag.png", 0)
    height, width = img.shape
    U, V = np.where(img < 128)
    U = U.astype(np.float32) / height
    V = V.astype(np.float32) / width * 5

    vecs = ortho_group.rvs(DIM)
    coords = U.reshape(-1, 1) * vecs[0] + V.reshape(-1, 1) * vecs[1]
    coords = shuffle(coords, vecs[2])
    coords = shuffle(coords, vecs[3])
    coords = coords[np.random.permutation(len(coords))]
    np.save("problem.npy", coords)
