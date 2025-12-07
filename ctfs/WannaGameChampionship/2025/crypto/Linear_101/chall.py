import random
import os

n = 128
random.seed("Wanna Win?")

def encrypt(A, x):
    b = [0] * n
    for i in range(n):
        for j in range(n):
            b[i] = max(b[i], A[i][j] + x[j])
    return b

def game():
    for round in range(64):
        try:
            print(f"Round {round+1}/64")
            A = [random.randbytes(n) for _ in range(n)]
            x = os.urandom(128)
            b = encrypt(A, x)

            print(f"{b = }")
            sol = bytes.fromhex(input("x = "))
            if len(sol) != n:
                return False
            
            if encrypt(A, sol) != b:
                print("Wrong!")
                return False
        except:
            return False
    return True

if game():
    print(open("flag.txt", "r").read())
else:
    print("You lose...")
