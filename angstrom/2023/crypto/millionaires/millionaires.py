#!/usr/local/bin/python

import private_set_intersection.python as psi
import base64
import secrets

def fake_psi(a, b):
    return [i for i in a if i in b]


def zero_encoding(x, n):
    ret = []

    s = bin(x)[2:].zfill(n)

    for i in range(n):
        if s[i] == "0":
            ret.append(s[:i] + "1")

    return ret


def one_encoding(x, n):
    ret = []

    s = bin(x)[2:].zfill(n)

    for i in range(n):
        if s[i] == "1":
            ret.append(s[:i+1])

    return ret


def performIntersection(serverInputs):
    s = psi.server.CreateWithNewKey(True)
    numClientElements = int(input("Size of client set: "))

    setup = s.CreateSetupMessage(0.001, numClientElements, serverInputs, psi.DataStructure.RAW)

    print("Setup: ", base64.b64encode(setup.SerializeToString()).decode())

    req = psi.Request()
    req.ParseFromString(base64.b64decode(input("Request: ")))

    resp = psi.Response()
    resp.ParseFromString(s.ProcessRequest(req).SerializeToString())
    print(base64.b64encode(resp.SerializeToString()).decode())


def ensure_honesty(secret, history):
    print("Okay, game time's over. Hand over your inputs and let's see if you cheated me.")
    for i in history:
        x = int(input(": "))

        if sorted(fake_psi(one_encoding(secret, NBITS), zero_encoding(x, NBITS)), key=lambda _: len(_)) != sorted(i, key=lambda _: len(_)):
            print("Cheater! I'll have my people break your knees.")
            exit(2)



NBITS = 256
correct = 0

for i in range(10):
    print(f"Currently talking to millionaire {i+1}/10")
    tries = 0

    secret = secrets.randbits(NBITS)

    serverInputs = one_encoding(secret, NBITS)

    performIntersection(serverInputs)
    tries += 1
    
    history = []
    x = input("Computed intersection: ").split(" ")
    history.append(x if x != [''] else [])

    while tries < 215:
        performIntersection(serverInputs)

        x = input("Computed intersection: ").split(" ")
        history.append(x if x != [''] else [])

        tries += 1

        x = input("Check (y/N)? ")
        if x == "y":
            break


    if tries < 215 and int(input("My secret: ")) == secret:
        print(f"You guessed it!")
        ensure_honesty(secret, history)
        correct += 1

    else:
        print("death")
        exit()

if correct == 10:
    print(open("flag.txt").read())