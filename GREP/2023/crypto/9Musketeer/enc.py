# path.py
import numpy as np
import binascii

message = "REDACTED"
key = "Musketeer"

list = [message[i : i + 2] for i in range(0, len(message), 2)]
list = [eval(i) for i in list]
list2 = [key[i] for i in range(len(key))]

# print(list)
# print(list2)

val = [chr(x) for x in list]
# print(val)

new = [ord(i) ^ ord(j) for i, j in zip(list2, val)]
# print(new)

new_list = []
new_list2 = []
for word in new:
    c = 0
    if word >= 1:
        new_list.append(format(word, "08b"))

ctext = "".join(new_list)
# print(ctext)

cipher = [ctext[i : i + REDACTED ] for i in range(0, len(ctext), REDACTED)]
m1 = cipher[0]
m2 = cipher[1]
# print(m1)
# print(m2)

m3 = []
j = 0
k = 0
for i in range(2 * len(m1)):
    if i % 2 == 0:
        m3.append(m1[j])
        j += 1
    else:
        m3.append(m2[k])
        k += 1
m3 = "".join(m3)
print(m3)

# 010101111001000001001110001100110101110100111000011000001000111100100110 -> m3