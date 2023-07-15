#!/usr/local/bin/python
from Crypto.Util.number import *
from Crypto.Cipher import AES
from math import ceil
import os
import random
from flag import flag

xyz = len(flag)

fullkey = ""
for i in range(128):
    key = ""
    for j in range(128):
        key += str(random.randint(0, 1))
    for j in range(10):
        key = bin(int(key, 2))[:2:-1] + str(random.randint(0, 1))
    key = bin(int(key, 2))[:2:-1]
    key = int(key)
    key = pow(key, random.randint(0, 256), random.randint(1, 256))
    for i in range(256):
        key = key * i * random.randint(0, 2) + key * random.randint(
            1, 3) + key // (i + 1) * random.randint(2, 4) + key * key
        key = key % 256
        key = key * \
            random.randint(1, random.randint(
                1, random.randint(1, random.randint(1, 1e4))))
    key = bin(key)[2:][::-1]
    fullkey += key[0]
key = long_to_bytes(int(fullkey, 2))

# secure padding
key = b"\x00" * (16 - len(key)) + key
flag = b"\x00" * (16 - len(flag) % 16) + flag

iv = os.urandom(16)
aescbc = AES.new(key, AES.MODE_CBC, iv=iv)
encrypted_flag = aescbc.encrypt(flag).hex()

luck = 0


def draw():
    y = 1
    while random.randint(1, 10000) != 1:
        y += 1
    return y


while True:
    args = input("Enter Arguments: ")
    if args == "flag":
        if luck >= 3:
            print(encrypted_flag)
            break
        else:
            print("Not lucky enough.")
    elif args == "":
        print("Bruh please input something plz!!")
        break
    elif args == "draw":
        if random.randint(1, 10000) == 1:
            luck += 1
            if luck == 1:
                print("Success! 2 more draws until you can see the flag!")
            elif luck == 2:
                print("Success! 1 more draw until you can see the flag!")
            elif luck == 3:
                print("Success! Now go get that flag!")
                for i in range(random.randint(1, 8)):
                    print(random.randint(0, 1), end="")
                print()
            else:
                print("Your lucky number is:", bytes_to_long(
                    os.urandom(getRandomInteger(3))))
        else:
            print("Better luck next time!")
            break
    elif args[:3] == "win":
        if args[3:] == "":
            print("if you were to draw, you would've drawn", draw(), "times")
            break
        else:
            # good luck!
            if bytes_to_long(os.urandom(getRandomInteger(10))) == 69420**3:
                try:
                    print("good job. you won.")
                    print(eval(args[3:]))
                except:
                    print(
                        args[3:], "gave an error, too bad so sad. Try again next century. Maybe try printing the flag next time. ;) Just saying.")
            else:
                print("Didn't win hard enough, sorry.")
    elif args == "rsa":
        print(pow(bytes_to_long(flag), 3, getPrime(128)*getPrime(128)))
        print(pow(xyz, 3, getPrime(128)*getPrime(128)))
    # random way of getting you to minimize query count.
    elif ord(args[0]) % (getRandomInteger(7) + 1) == 3:
        print("Too many RNG calls!")
    else:
        try:
            assert str(int(args)) == args, "get better"
            if 0 < int(args) <= 128:
                print(random.randrange(1, 2**int(args)))
            elif int(args) > 128:
                print(random.randrange(1, len(str(args))))
            else:
                print("Invalid input")
        except:
            try:
                # limit loop length because it would be bad if it were uncapped.
                args = int(args[1:]) % 10**5
                for i in range(args):
                    random.randrange(1, 2)
            except:
                print("Invalid input.")
print("Exiting...")
