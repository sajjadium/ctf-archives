state = 1
flag = "[REDACTED]"
alphabet = "abcdefghijklmnopqrstuvwxyz"
assert(flag[0:5]+flag[-1]=="flag{}")
ciphertext = ""
for character in flag[5:-1]:
    state = (15*state+18)%29
    ciphertext+=alphabet[(alphabet.index(character)+state)%26]
print(ciphertext)