from hashlib import md5, sha256
import random
from Crypto.Util.number import *

alphanum = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

flag = "This flag has been REDACTED"
secret = ''.join(random.choices(alphanum,k=10))
sec_num = bytes_to_long(secret.encode())

history = []
tries = 3
while tries:
    print(f"Tries left : {tries}")
    print("Provide the hex of first message: ",end='')
    m1 = bytes.fromhex(input())
    print("Provide the hex of second message: ",end='')
    m2 = bytes.fromhex(input())
    if m1==m2:
        print("Do you take me as a fool?. Give me 2 different messages.\n")
        tries-=1
        continue
    if m1[0] in history or m2[0] in history:
        print("You have already provided messages with the same first byte. You still lose a try.\n")
        tries-=1
        continue
    if md5(m1).hexdigest()==md5(m2).hexdigest() and sha256(m1).hexdigest()[:5]==sha256(m2).hexdigest()[:5]:
        history.append(m1[0])
        print("Wow! Both messages have the same signature.")
        print("Okay I can reveal some part of the secret to you. Give me a number with no more than 24 set bits and I will reveal those bits of the secret to you.")
        print("num: ",end='')
        num = int(input())
        bit_count = bin(num).count('1')
        if bit_count>24:
            print("Read the rules properly. No more than 24 bits allowed.\n")
            tries-=1
            continue
        print(f"Revealing bits : {sec_num&num}\n")
        tries-=1
        continue
    else:
        print("The signatures don't match.\n")
        tries-=1
        continue

print("Can you Guess the secret: ",end='')
guess = input()
if guess == secret:
    print(f"You gussed correctly. Here is your flag: {flag}")
else:
    print(f"Wrong guess. Bye bye!")