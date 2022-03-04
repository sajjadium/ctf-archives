from PIL import Image

im = Image.open("flag.png")

col,row = im.size

pix = im.load()

key = ''
k = []

for i in key:
    k.append(ord(i))

enc = Image.new(im.mode,im.size)
out = enc.load()

for i in range(col):
    for j in range(row):
        ca = (k[0] + k[1]*i) % col
        ra = (k[2] + k[3]*j) % row
        out[ca,ra] = pix[i,j]

for i in range(0,col,2):
    for j in range(0,row,2):
        out[i,j] = out[i,j] ^ k[4]
        out[i+1,j] = out[i+1,j] ^ k[5]
        out[i,j+1] = out[i,j+1] ^ k[6]
        out[i+1,j+1] = out[i+1,j+1] ^ k[7]

enc.save("enc.png")
