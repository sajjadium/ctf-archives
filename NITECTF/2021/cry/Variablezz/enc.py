import random
flag = 'nite{XXXXXXXXXXXXXXXXXXXXXXXX}'
a = random.randint(1,9999999999)
b = random.randint(1,9999999999)
c = random.randint(1,9999999999)
d = random.randint(1,9999999999)
enc = []
for x in flag:
    res = (a*pow(ord(x),3)+b*pow(ord(x),2)+c*ord(x)+d)
    enc.append(res)
print(enc)