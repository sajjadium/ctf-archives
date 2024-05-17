from PIL import Image

import random

random.seed(42)

lmao = random.randint(12345678,123456789)

random.seed(lmao)

img = Image.open("skibidi.png")

width, height = img.size

flag = open("flag.txt", "rb").read()

st = ""
for i in bytearray(flag):
    tmp = bin(i)[2:]
    while(len(tmp))<8:
        tmp = "0"+tmp
    st+=tmp

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

inds = [i for i in range(288)]

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

randnum = random.randint(1,500)

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

for i in range(random.randint(0,500), random.randint(500,1000)):
    random.seed(i)
    random.shuffle(inds)
    if i==randnum:
        break

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

new_flag = "".join([st[i] for i in inds])

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

troll = [random.randint(random.randint(-lmao,0),random.randint(0,lmao)) for _ in range(random.randint(1,5000))]

troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

pic_inds = []
while len(pic_inds)!=288:
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    pic_inds.append(random.randint(0,width*height))
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))

for i in range(288):
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    cur_ind = pic_inds[i]
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    row = cur_ind//height
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    col = cur_ind%width
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    colors = list(img.getpixel((row,col)))
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    change = random.randint(0,2)
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    colors[change] = (colors[change]& 0b11111110) | int(new_flag[i])
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    img.putpixel((row,col),tuple(colors))
    troll = random.randint(random.randint(-lmao,0),random.randint(0,lmao))
    if(i%randnum==0):
        random.seed(random.randint(random.randint(-lmao,0),random.randint(0,lmao)))

img.save("skibidi_encoded.png")

