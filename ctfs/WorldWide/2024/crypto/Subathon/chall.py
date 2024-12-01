from notaes import notAES
from os import urandom
from time import time


# ugh standard flag shenanigans yada yada
key = urandom(16)
cipher = notAES(key)

from secret import flag
flag_enc = cipher.encrypt(flag.encode())
print(f'{flag_enc = }')


# time for the subathon!
st = time()
TIME_LEFT = 30
while time() - st < TIME_LEFT:
    print("=================")
    print("1. Subscrib")
    print("2. Play rand gaem")
    print("3. Quit")
    print("=================")
    choice = str(input())
    if choice == "1":
        print("Thank you for the sub!!")
        TIME_LEFT += 30
    elif choice == "2":
        print("Guess the number!")
        ur_guess = int(input(">> "))
        my_number = int.from_bytes(cipher.encrypt(urandom(16)), "big")
        if ur_guess != my_number:
            print(f"You lose, the number was {my_number}")
        else:
            print("Omg you won! Here's the flag")
            print(flag)
    else:
        break
print("The subathon's over! Hope you had fun!!")