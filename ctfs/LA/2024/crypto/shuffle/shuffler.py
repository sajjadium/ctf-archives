#!/usr/local/bin/python3

from secrets import randbits
import math
from base64 import b64encode
MESSAGE_LENGTH = 617

class LCG:

    def __init__(self,a,c,m,seed):
        self.a = a
        self.c = c
        self.m = m
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

def generate_random_quad():
    return randbits(64),randbits(64),randbits(64),randbits(64)

initial_iters = randbits(16)

def encrypt_msg(msg, params):
    global initial_iters
    a, c, m, seed = params
    L = LCG(a, c, m, seed)
    for i in range(initial_iters):
        L.next()
    l = len(msg)
    permutation = []
    chosen_nums = set()
    while len(permutation) < l:
        pos = L.next() % l
        if pos not in chosen_nums:
            permutation.append(pos)
            chosen_nums.add(pos)
    output = ''.join([msg[i] for i in permutation])
    return output

# period is necessary
secret = b64encode(open('secret_message.txt','rb').read().strip()).decode() + '.'
length = len(secret)
assert(length == MESSAGE_LENGTH)

a, c, m, seed = params = generate_random_quad()
enc_secret = encrypt_msg(secret,params)

while True:
    choice = input("What do you want to do?\n1: Shuffle a message.\n2: Get the encrypted secret.\n3: Quit.\n> ")
    if choice == "1":
        message = input("Ok. What do you have to say?\n")
        if (len(message) >= length):
            print("I ain't reading allat.\n")
        elif (math.gcd(len(message),m) != 1):
            print("Are you trying to hack me?\n")
        else:
            print(f"Here you go: {encrypt_msg(message,params)}\n")
    elif choice == "2":
        print(f"Here you go: {enc_secret}\n")
    elif choice == "3":
        print("bye bye")
        exit(0)
    else:
        print("Bad choice.\n")

