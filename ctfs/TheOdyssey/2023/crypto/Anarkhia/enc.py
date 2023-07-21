#!/usr/bin/python3

import random
from secret import flag

random.seed(''.join([str(random.randint(0x0, 0x9)) for i in range(random.randint(3, 6))]));theKey = [random.randint(0, 255) for i in range(len(flag))];theEnc = "".join([hex(((random.choice(theKey)) ^ ord(flag[i]))<<1) for i in range(len(flag))]);open('out.txt', 'w').write(theEnc)