import random

secret = 'XXXXXXXXXXXXXXXXXXXX'

PINK = 118
RED = 101
YELLOW = 97
GREEN = 108
BLACK = __builtins__
PURPLE = dir
e = getattr(BLACK, bytes([RED, PINK, YELLOW, GREEN]).decode())
g = e(''.__dir__()[4].strip('_')[:7])
b = g(BLACK, PURPLE(BLACK)[92])
i = g(BLACK, PURPLE(BLACK)[120])
t = ['74696d65', '72616e646f6d', '5f5f696d706f72745f5f', '726f756e64', '73656564']
d = lambda x: b.fromhex(x).decode()
fb = g(i, PURPLE(i)[-6])
_i = lambda x: e(d(t[2]))(x)
s = lambda: g(BLACK,d(t[3]))(g(_i(d(t[0])), d(t[0]))()) + fb(secret.encode())
r = g(_i(d(t[1])), d(t[4]))

def kg(l):
    return bytes([random.randint(0,255) for i in range(l)])

def c(p):
    k = kg(len(p))
    return bytes([k[i] ^ p[i] for i in range(len(p))]).hex()

if __name__ == '__main__':
    r(s())
    print("Welcome to our encryption service.")
    choice = input("Choose between:\n1. Encrypt your message.\n2. Get the encrypted secret.\nEnter your choice: ")
    match choice:
        case "1":
            message = input("Please enter the message you wish to encrypt: ")
            print(f"Your encrypted message is: {c(message.encode())}")
        case "2":
            print(f"The secret is: {c(secret.encode())}")
        case _:
            print("Invalid option!")