#!/usr/local/bin/python3

from secret import flag
from Crypto.Util.number import *


jokes = [
    "Why did the prime break up with the modulus? Because it wasn't factoring in its feelings",
    "Why did the cryptographer bring RSA to the dance? Because it had great curves — wait, no, wrong cryptosystem",
    "Why did the CTF player cross the road? To get to the " + flag,
]

def hideFlag(message):
    hidden = ""
    start = False
    for c in message:
        if (start):
            hidden += "X"
        else:
            hidden += c
        if c == "{":
            start = True
    if (start):
        hidden = hidden[:-1] + "}"
    return hidden

def run():
    print("You think you're funny? I got a few jokes of my own, tell me a joke and I'll tell you mine")
    transcript = []
    for i in range(3):
        joke = input("Tell me a joke: ")
        funny = bytes_to_long(joke.encode()) % 2
        if (not funny):
            print("Really? That's it? Come back with some better material")
            exit()
        else:
            transcript.append(joke)
            print("Ha! That was pretty funny! Here's one of my own")
            print(hideFlag(jokes[i]))
            transcript.append(jokes[i])
    print("Here is our jokes! Show it to a friend to make them laugh! I better encrypt it though in case I said something private")

    m = "\n".join(transcript)
    
    p = getPrime(512)
    q = getPrime(512)
    N = p * q
    
    e = 3
    c = pow(bytes_to_long(m.encode()), e, N)
    print("c =", c)
    print("N =", N)
    print("e =", e)

if __name__ == '__main__':
    run()
