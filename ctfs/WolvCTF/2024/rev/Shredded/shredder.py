import random

with open(".\\shredded.c", "r") as f:
    lines = f.readlines()

longest = 0

for i in lines:
    i = i.replace("\n", " ")
    if len(i) > longest:
        longest = len(i)

padLines = []

for i in lines:
    padLines.append(i.replace("\n"," ") + " " * (longest - len(i)))
    print(i)

split = ["" for _ in range(longest)]

for line in padLines:
    for i in range(longest):
        split[i] += line[i]
        split[i] += "\n"

split.pop()

random.shuffle(split)

'''for j in range(len(split[0])):
    for i in split:
        if i[j] != "\n":
            print(i[j], end="")
    print()'''
#block to print out the shredded file

for i in range(len(split)):
    fname = ".\\shredFiles\\shred" + str(i) + ".txt"
    with open(fname, "w") as f:
        f.write(split[i])

print("Shredded file into " + str(longest-1) + " shreds")