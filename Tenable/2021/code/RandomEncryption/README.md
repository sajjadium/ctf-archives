

We found the following file on a hacked terminal:

import random
flag = "flag{n0t_that_r4ndom}"
seeds = []
for i in range(0,len(flag)):
    seeds.append(random.randint(0,10000))

res = []
for i in range(0, len(flag)):
    random.seed(seeds[i])
    rands = []
    for j in range(0,4):
        rands.append(random.randint(0,255))

    res.append(ord(flag[i]) ^ rands[i%4])
    del rands[i%4]
    print(str(rands))

print(res)
print(seeds)

We also found sample output from a previous run:

[22, 67, 142]
[57, 51, 53]
[97, 114, 14]
[16, 94, 107]
[187, 79, 172]
[138, 138, 118]
[32, 41, 8]
[93, 104, 248]
[112, 33, 215]
[22, 163, 8]
[170, 21, 156]
[183, 196, 255]
[62, 160, 64]
[93, 124, 68]
[53, 227, 187]
[234, 44, 74]
[96, 171, 138]
[161, 46, 45]
[186, 114, 154]
[188, 137, 120]
[239, 44, 13]
[209, 17, 111, 78, 180, 98, 205, 186, 202, 124, 139, 37, 57, 95, 47, 136, 114, 168, 139, 204, 165]

Can you decode it?

