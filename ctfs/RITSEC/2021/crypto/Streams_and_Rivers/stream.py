import random
import os
import binascii
import sys

a = long(binascii.hexlify(os.urandom(2500)), 16)
rand = random.Random(a)
flag = "__RS{REDACTEDREDACTEDRED}" #only difference between this and challenge binary is the characters of the flag were replaced with the characters of redacted

def transform(x):
    unshiftRight = lambda res,next : x^(res>>next)
    makeUnshiftLeft = lambda mask: lambda res,next : x^(res << next & mask)
    makeList = lambda x: [x for i in range(32)] 

    x = reduce(unshiftRight, makeList(18))
    x = reduce(makeUnshiftLeft(0xefc60000), makeList(15))
    x = reduce(makeUnshiftLeft(0x9d2c5680), makeList(7))
    x = reduce(unshiftRight, makeList(11))

    return x

def make_plaintext(padlen, num_iters=8):
    #Make sure the padlen is reasonable.
    #We pad num_iters times with padlen repeated random characters 
    if padlen*num_iters > 325:
        padlen = 325/num_iters
        print("Too much padding, shortening padding")
    if padlen < len(flag):
        padlen = len(flag)
        print("Too little padding, lengthening padding")
    
    gen_rand = random.Random()
    padding = ""
    for i in range(num_iters):
        padding += chr(gen_rand.getrandbits(8))*padlen
    
    #Make our message even longer, just to show the strength
    padded_msg = (flag + padding)
    plaintext = padded_msg
    while(len(plaintext) < 2600):
        plaintext += padded_msg[:2600-len(plaintext)]
    return plaintext

def encrypt(plaintext):
    ct = []
    pos = 0
    while pos < len(plaintext):
        rand_int = rand.getrandbits(32)
        trand_int = transform(rand_int)
        for j in range(4):
            if pos >= len(plaintext):
                break
            rand_short = (trand_int >> (j*8)) & 0xff
            ct.append(rand_short ^ ord(plaintext[pos]))
            pos += 1
    return ct

print("Welcome to my advanced encryption service")
print("I have a new super secure stream cipher.")
print("One thing that it really needs is padding. I'll let let you chose how much of that to add.")
print("Don't try any of those buffer overflow tricks though. You can only ask for so much padding")
print("Just to show the strength of my cipher, I'll encrypt the message a few times and give you the result.")
print("So how much padding should I use?")
sys.stdout.flush()

padlen = int(sys.stdin.readline())
plaintext = make_plaintext(padlen)
ct = encrypt(plaintext)

print("Here your encrypted message is")
print((''.join([chr(x) for x in ct])).encode("hex"))
