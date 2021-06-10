from string import ascii_letters, digits
from random import SystemRandom
from math import ceil, log
from signal import signal, alarm, SIGALRM
from secret import flag

random = SystemRandom()
ALPHABET = ascii_letters + digits + "_!@#$%.'\"+:;<=}{"
shuffled = list(ALPHABET)

random.shuffle(shuffled) 
S_box = {k : v for k, v in zip(ALPHABET, shuffled)} 

def encrypt(message):
    if len(message) % 2:
        message += "_"

    message = list(message)
    rounds = int(2 * ceil(log(len(message), 2))) 

    for round in range(rounds):
        message = [S_box[c] for c in message]
        if round < (rounds-1):
            message =  [message[i] for i in range(len(message)) if i%2 == 1] + [message[i] for i in range(len(message)) if i%2 == 0]
    return ''.join(message)

def play():
    print("Here's the flag, please decrypt it for me:")
    print(encrypt(flag))

    for _ in range(150):
        guess = input("> ").strip()
        assert 0 < len(guess) <= 10000

        if guess == flag:
            print("Well done. The flag is:")
            print(flag)
            break

        else:
            print("That doesn't look right, it encrypts to this:")
            print(encrypt(guess))

def timeout(a, b):
    print("\nOut of time. Exiting...")
    exit()

signal(SIGALRM, timeout) 
alarm(5 * 60) 

play()
