from PIL import Image
import numpy as np
import cv2
FILE = 'original.png'
img = Image.open(FILE)
arr = np.asarray(img, dtype=np.float64)
grayArr = np.zeros((len(arr), len(arr[0])))
for vert in range(len(arr)):
    for hori in range(len(arr[0])):
        grayArr[vert][hori] = arr[vert][hori]
nHeight = len(grayArr) - len(grayArr) % 8
nWidth = len(grayArr[0]) - len(grayArr[0]) % 8
cropArr = np.zeros((nHeight, nWidth)) # resize dumb
for i in range(0, nHeight):
    for j in range(0, nWidth):
        cropArr[i,j] = grayArr[i,j] / 2# - 128
grayArr = cropArr
dctArr = np.zeros((nHeight, nWidth))
def dct2(arr):
    return cv2.dct(arr/255)*255
dctArr = np.zeros((nHeight, nWidth))
for i in range(0, nHeight, 8):
    for j in range(0, nWidth, 8):
        dctArr[i:i+8,j:j+8] = dct2(grayArr[i:i+8,j:j+8])
scalar = np.array([16, 11, 10, 16, 24, 40, 51, 61,
                   12, 12, 14, 19, 26, 58, 60, 55,
                   14, 13, 16, 24, 40, 57, 69, 56,
                   14, 17, 22, 29, 51, 87, 80, 62,
                   18, 22, 37, 56, 68, 109,103,77,
                   24, 35, 55, 64, 81, 104,113,92,
                   49, 64, 78, 87, 103,121,120,101,
                   72, 92, 95, 98, 112,100,103,99])
scalar = scalar.reshape((8, 8))
reduArr = np.zeros((nHeight, nWidth))
for i in range(0, nHeight, 8):
    for j in range(0, nWidth, 8):
        block = np.array(dctArr[i:i+8,j:j+8])
        reduArr[i:i+8,j:j+8] = np.divide(block, scalar)
for i in range(0, nHeight):
    for j in range(0, nWidth):
        reduArr[i,j] = reduArr[i,j].round()
        if reduArr[i,j] == 0:
            reduArr[i,j] = 0
order = [0, 1, 8, 16, 9, 2, 3, 10, 17, 24, 32, 25, 18, 11, 4, 5, 12, 19, 26, 33, 40, 48, 41, 34, 27, 20, 13, 6, 7, 14, 21, 28, 35, 42, 49, 56, 57, 50, 43, 36, 29, 22, 15, 23, 30, 37, 44, 51, 58, 59, 52, 45, 38, 31, 39, 46, 53, 60, 61, 54, 47, 55, 62, 63]
result = ''
for i in range(0, nHeight, 8):
    for j in range(0, nWidth, 8):
        toBeRead = reduArr[i:i+8, j:j+8].flatten()
        for index in order:
            num = toBeRead[index]
            if num >= 0: sign = '0'
            else: sign = '1'
            result += f'{sign}{int(abs(toBeRead[index])):07b}'
compressed_value = f'0{nHeight:07b}0{nWidth:07b}{result}'
f = open("flag", "wb")
f.write(int("".join(compressed_value),2).to_bytes(len(compressed_value)//8, byteorder="big"))