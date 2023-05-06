from sympy import poly, symbols
from collections import deque
import Crypto.Random.random as random
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def build_poly(coeffs):
    x = symbols('x')
    return poly(sum(coeff * x ** i for i, coeff in enumerate(coeffs)))

def encrypt_msg(msg, poly, e, N):
    return long_to_bytes(pow(poly(msg), e, N)).hex()

p = getPrime(256)
q = getPrime(256)
N = p * q
e = 11

flag = bytes_to_long(open("/challenge/flag.txt", "rb").read())

coeffs = deque([random.randint(0, 128) for _ in range(16)])


welcome_message = f"""
Welcome to RotorSA!
With our state of the art encryption system, you have two options:
1. Encrypt a message
2. Get the encrypted flag
The current public key is
n = {N}
e = {e}
"""

print(welcome_message)

while True:
    padding = build_poly(coeffs)
    choice = int(input('What is your choice? '))
    if choice == 1:
        message = int(input('What is your message? '), 16)
        encrypted = encrypt_msg(message, padding, e, N)
        print(f'The encrypted message is {encrypted}')
    elif choice == 2:
        encrypted_flag = encrypt_msg(flag, padding, e, N)
        print(f'The encrypted flag is {encrypted_flag}')
    coeffs.rotate(1)