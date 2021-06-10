from random import randint
from secret import flag, solvable
from signal import signal, alarm, SIGALRM

class lsfr:
    def __init__(self):
        self.state = [randint(0, 5039) for _ in range(10)]
        while True:
            self.coefs = [randint(0, 5039) for _ in range(10)]
            if solvable(self): break

    def next(self):
        n = sum([self.state[i] * self.coefs[i] for i in range(10)]) % 5039
        self.state = self.state[1:] + [n]
        return n

def check(pin, guess):
    a = 0
    b = 0
    for i in range(len(guess)):
        if guess[i] in pin:
            if pin.index(guess[i]) == i: a += 1
            else: b += 1
    return [a,b]

def unique(n):
    return len(set("%04d" % n)) == 4

def play():
    i = 0
    print("Flag is locked under %d pins, you have %d guesses." % (N, r))

    for _ in range(r):
        guess = input("Enter pin %d:\n>" % (i+1))
        a, b = check(pins[i], guess)
        if a == 4 and b == 0:
            i += 1
            if i == N:
                print("Congratulations! Here is the flag: %s" % flag)
                return
            else:
                print("Correct, onto the next one!")
        else: 
            print("Wrong! Hint: A%dB%d" % (a,b))

    print("Out of guesses, exiting...")


def timeout(a, b):
    print("\nOut of time. Exiting...")
    exit()

signal(SIGALRM, timeout) 
alarm(5 * 60) 

rng = lsfr()
r = 260
N = 200

all = ["%04d" % n for n in range(10000) if unique(n)]

pins = [all[rng.next()] for _ in range(N)]

play()
