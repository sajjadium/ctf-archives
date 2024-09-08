from secret import flag

p = 4066351909

for f in flag:
    print((ord(f)*2022684581 - 127389238) % p, end=",")