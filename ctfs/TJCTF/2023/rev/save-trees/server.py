#!/usr/local/bin/python3.10 -u

import ast
import sys

import select
from Crypto.Util.number import bytes_to_long
import hashlib
import random


def set_globals():
    global edge_lst, cnt, threshold, vals, key, lvs
    edge_lst = []
    cnt, threshold = 0, 128
    vals = [0 for _ in range(threshold*16)]
    key = (bytes_to_long(bytes('save thr trees!!', 'utf-8'))
           << 16) + random.randint((1 << 15), (1 << 16))
    lvs = []


with open('flag.txt', 'r') as f:
    flag = f.readline()


def ear3mt3sdk(nd):
    global cnt, threshold, edge_lst, lvs, key
    if nd > threshold:
        lvs.append(nd)
        return
    if nd > threshold // 2:
        if random.randint(1, 4) == 1:
            lvs.append(nd)
            return
    edge_lst.append((nd, cnt+1))
    edge_lst.append((nd, cnt+2))
    old_cnt = cnt
    vals[cnt+1] = (vals[nd] >> 16) ^ key
    vals[cnt+2] = (vals[nd] & ((1 << 16) - 1)) ^ key
    cnt += 2
    ear3mt3sdk(old_cnt+1)
    ear3mt3sdk(old_cnt+2)


set_globals()
hsh = int('0x10000000' + str(hashlib.sha256(flag.encode('utf-8')).hexdigest()), 16)
vals[0] = hsh
ear3mt3sdk(0)

print('you have 5s to help treeelon musk save the trees!!')
print(edge_lst)
print([(nd, vals[nd]) for nd in lvs])


def input_with_timeout(prompt, timeout):
    sys.stdout.write(prompt)
    sys.stdout.flush()
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')
    raise Exception


try:
    answer = input_with_timeout('', 5)
except:
    print("\nyou let treeelon down :((")
    exit(0)

try:
    answer = ast.literal_eval(answer)
except:
    print("treeelon is very upset")
    exit(0)

if hsh == answer:
    print('good job treeelon is proud of you <3<3')
    print(flag)
else:
    print("treeelon is upset")
