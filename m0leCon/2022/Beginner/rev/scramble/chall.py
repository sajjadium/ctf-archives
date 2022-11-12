from flag import flag
from random import randint

assert(len(flag) <= 50)
shift = randint(1, len(set(flag)) - 1)

def encrypt(data):
    charsf = {}
    for c in data:
        if c not in charsf.keys():
            charsf[c] = 1
        else:
            charsf[c] += 1

    chars = list(charsf.keys())
    chars.sort(reverse=True, key=lambda e: charsf[e])

    charsn = list(chars)
    for _ in range(shift):
        i = charsn.pop(0)
        charsn.append(i)

    enc = "".join(list(map(lambda c: charsn[chars.index(c)], data)))
    return enc

if __name__ == "__main__":
    print("Welcome to our custom encrypting system!")
    print("1) Encrypt something")
    print("2) Get flag")
    print("3) Exit")

    opt = input("> ")
    while opt != "3":
        if opt == "1":
            data = input("What is your string?\n")
            print(encrypt(data))
        elif opt == "2":
            print(encrypt(flag))
        opt = input("> ")
