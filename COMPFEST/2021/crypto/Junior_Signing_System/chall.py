#!/usr/bin/env python3

from collections import namedtuple
from Crypto.Util.number import inverse, bytes_to_long
from Crypto.Hash import SHA1
import sys
import os

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def add(first, second):
    global p
    return ((first % p) + (second % p)) % p

def subtract(first, second):
    global p
    return (first % p - second % p + p) % p

def multiply(first, second):
    global p
    return ((first % p) * (second % p)) % p

def divide(first, second):
    global p
    return multiply(first, inverse(second, p))

def point_addition(P, Q):
    global p, a

    if (P.x == 0 and P.y == 0):
        return Q
    if (Q.x == 0 and Q.y == 0):
        return P
    
    x1, y1, x2, y2 = P.x, P.y, Q.x, Q.y
    
    if (x1 == x2 and (y1 + y2) % p == 0):
        return Point(0, 0)
    
    if (x1 != x2 or y1 != y2):
        res = divide(subtract(y2, y1), subtract(x2, x1))
    else:
        res = divide(add(multiply(3, multiply(x1, x1)), a), multiply(2, y1))
    
    x3 = subtract(subtract(multiply(res, res), x1), x2)
    y3 = subtract(multiply(res, subtract(x1, x3)), y1)
    return Point(x3, y3)

def scalar_multiplication(k, P):
    global Point

    Q = Point(0, 0)
    k = bin(k)[2:]
    
    for k_i in k:
        Q = point_addition(Q, Q)
        if (k_i == '1'):
            Q = point_addition(Q, P)
        
    return Q

def special_scalar_multiplication(k, P, feature):
    global Point

    Q = Point(0, 0)
    Q_special = Point(0, 0)
    k = bin(k)[2:]
    t = len(k)
    
    for k_i in k:
        Q = point_addition(Q, Q)
        if (feature != t):
            Q_special = point_addition(Q_special, Q_special)

        if (k_i == '1'):
            Q = point_addition(Q, P)
            Q_special = point_addition(Q_special, P)

        t -= 1

    return Q, Q_special

def sign_a_message():
    global d, n, P, Q, Point, p, a, b

    print('Public key:')
    print('E = x**3 + %d*x + %d' % (a, b) )
    print('P =', P)
    print('n =', n)
    print('Q =', Q)

    message = input('Your message: ')
    message = message.encode()
    want = input('Want to try the special feature? (y/n): ')

    while True:
        k = bytes_to_long(os.urandom(20))
        if not(1 <= k <= n-1):
            continue
        if (want == 'y'):
            feature = bytes_to_long(os.urandom(20)) % 5 + 12
            T, T_special = special_scalar_multiplication(k, P, feature)
        else:
            T, T_special = special_scalar_multiplication(k, P, None)
        gamma = T.x % n
        gamma_special = T_special.x % n
        if (gamma == 0):
            continue
        
        hash = SHA1.new()
        hash.update(message)
        hash = bytes_to_long(hash.digest()) % n

        delta = (((hash + gamma * d) % n) * inverse(k, n)) % n
        delta_special = (((hash + gamma_special * d) % n) * inverse(k, n)) % n
        if (delta == 0):
            continue

        if (want == 'y'):
            print('Your special: (%d, %d, %d)' % (gamma_special, delta_special, delta))
        else:
            print('Your signature: (%d, %d)' % (gamma, delta))
        return
    
def verify_signature():
    global d, n, P, Q, Point, p, a, b

    print('Public key:')
    print('E = x**3 + %d*x + %d' % (a, b) )
    print('P =', P)
    print('n =', n)
    print('Q =', Q)

    message = input('Your message: ')
    message = message.encode()

    signature = input('Your signature: ')
    gamma, delta = map(int, signature[1:-1].split(', '))
    if not(1 <= gamma <= n - 1 and 1 <= delta <= n - 1):
        print('Not verified.')
        return
    
    w = inverse(delta, n)
    hash = SHA1.new()
    hash.update(message)
    hash = bytes_to_long(hash.digest()) % n
    u1 = (hash * w) % n
    u2 = (gamma * w) % n
    omega = point_addition(scalar_multiplication(u1, P), scalar_multiplication(u2, Q))
    
    if (not(omega.x == 0 and omega.y == 0) and (gamma == omega.x % n)):
        print('Verified.')
    else:
        print('Not verified.')

def print_menu():
    print()
    print('1. Sign a message')
    print('2. Verify signature')
    print('3. Exit')

def welcome():
    print('Welcome!')
    
    flag = b'REDACTED'
    assert len(flag) <= 20
    
    global d, n, P, Q, Point, p, E, a, b

    Point = namedtuple('Point', 'x y')

    p = 0xE95E4A5F737059DC60DFC7AD95B3D8139515620F
    a = 0x340E7BE2A280EB74E2BE61BADA745D97E8F7C300
    b = 0x1E589A8595423412134FAA2DBDEC95C8D8675E58
    assert 4 * (a ** 3) + 27 * (b ** 2) != 0
    E = lambda x : (x**3 + a*x + b) % p

    d = bytes_to_long(flag)
    x = 0xBED5AF16EA3F6A4F62938C4631EB5AF7BDBCDBC3
    y = 0x1667CB477A1A8EC338F94741669C976316DA6321
    n = 0xE95E4A5F737059DC60DF5991D45029409E60FC09
    P = Point(x, y)
    Q = scalar_multiplication(d, P)

def main():
    try:
        welcome()
        while True:
            print_menu()
            choice = int(input('> '))
            if (choice == 1):
                sign_a_message()
            if (choice == 2):
                verify_signature()
            if (choice == 3):
                print('Bye.')
                break
    except:
        print('An error occured.')
    exit(0)

if __name__ == '__main__':
    main()