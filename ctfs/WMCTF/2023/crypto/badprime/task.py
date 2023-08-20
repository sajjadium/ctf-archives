from Crypto.Util.number import *
from secret import flag

M = 0x7cda79f57f60a9b65478052f383ad7dadb714b4f4ac069997c7ff23d34d075fca08fdf20f95fbc5f0a981d65c3a3ee7ff74d769da52e948d6b0270dd736ef61fa99a54f80fb22091b055885dc22b9f17562778dfb2aeac87f51de339f71731d207c0af3244d35129feba028a48402247f4ba1d2b6d0755baff6

def getMyprime(BIT):
    while True:
        p = int(pow(65537, getRandomRange(M>>1, M), M)) + getRandomInteger(BIT-int(M).bit_length()) * M
        if isPrime(p):
            return p

p = getMyprime(1024)
q = getPrime(1024)
n = p * q
m = bytes_to_long(flag)

print("Try to crack the bad RSA")
print("Public key:", n)
print("The flag(encrypted):", pow(m, 65537, n))
print("Well well, I will give you the hint if you please me ^_^")
leak = int(input("Gift window:"))
if M % leak == 0:
    print("This is the gift for you: ", p % leak)
else:
    print("I don't like this gift!")