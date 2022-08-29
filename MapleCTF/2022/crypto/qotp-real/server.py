from random import uniform
from math import sin, cos, tan, pi
from signal import alarm
from secret import FLAG

EPS = 1e-9

class Qstate:
    def __init__(self, x: float, y: float):
        assert(abs(x * x + y * y - 1.0) < EPS)
        self.x = x
        self.y = y

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y


class Base:
    def __init__(self, q1: Qstate, q2: Qstate):
        assert(abs(q1 * q2) < EPS)
        self.q1 = q1
        self.q2 = q2

    def measure(self, q: Qstate):
        alpha = (self.q1 * q)**2
        return int(uniform(0, 1) >= alpha)


def get_random_bases(n: int):
    angles = [pi / 4 * uniform(-pi, pi) + pi / 4 for _ in range(n)]
    bases = [Base(Qstate(cos(angle), sin(angle)), Qstate(-sin(angle), cos(angle))) for angle in angles]
    return bases


def binify(s: str):
    return ''.join(format(ord(c), '08b') for c in s)

def decode(enc, bases):
    return ''.join(str(b.measure(q)) for q, b in zip(enc, bases))

def encode(msg, bases):
    enc = [b.q1 if x == '0' else b.q2 for x, b in zip(msg, bases)]
    assert decode(enc, bases) == msg
    return enc

def print_menu():
    print('''
What would you like to do?
(1) Encrypt message
(2) Decrypt message
(3) Decrypt flag
''')

def read_base():
    baseq1x = float(input("Enter base.q1.x: "))
    baseq1y = float(input("Enter base.q1.y: "))
    baseq2x = float(input("Enter base.q2.x: "))
    baseq2y = float(input("Enter base.q2.y: "))
    return Base(Qstate(baseq1x, baseq1y), Qstate(baseq2x, baseq2y))


if __name__ == '__main__':
    alarm(60)

    FLAG = binify(FLAG)
    enc = encode(FLAG, get_random_bases(len(FLAG)))
    msg = ""
    print("Welcome to my REAL quantum encryption service!")
    print("Only real numbers allowed!")
    while True:
        print_menu()
        response = int(input("Enter choice: "))
        if response == 1:
            msg = input("Enter message: ")
            msg = binify(msg)
            bases = [read_base()] * len(msg)
            msg = encode(msg, bases)
            print("Message stored!")
        elif response == 2:
            bases = [read_base()] * len(msg)
            print(decode(msg, bases))
        elif response == 3:
            bases = [read_base()] * len(FLAG)
            print(decode(enc, bases))
            enc = encode(FLAG, get_random_bases(len(FLAG)))

