import string

with open("key.txt", "r") as f:
    shift = int(f.readline())
    key = f.readline()

with open("flag.txt", "r") as f:
    flag = f.read()


stdalph = string.ascii_lowercase
rkey = ""

for i in key:
    if i not in rkey:
        rkey += i
for i in stdalph:
    if i not in rkey:
        rkey += i
rkey = rkey[-shift:] + rkey[:-shift]

enc = ""
for a in flag:
    if a in stdalph:
        enc += rkey[stdalph.index(a)]
    else:
        enc += a

print(enc)