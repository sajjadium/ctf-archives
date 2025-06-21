#!/usr/bin/env python3
from secret_params import curve_p, a, b, order, secret_point_x, secret_point_y
import os

FLAG = os.getenv("FLAG", "corn{__redacted_redacted_redacted__redacted_redacted_redacted__}").encode()

assert FLAG.startswith(b"corn{") and FLAG.endswith(b"}")
assert len(FLAG) == 64

def sign(m, x):
    if m == 0 or m == 1 or m == n-1:
        print("No weak messages allowed here")
        return None
    try:
        user_point = E.lift_x(x)
    except ValueError:
        print(f"Invalid point: {x} does not describe any point on the curve")
        return None
    sig = pow(m, d, n)
    sig = sig * user_point + secret_point
    return sig.xy()[0], sig.xy()[1]

def verify(sig, m, x):
    try:
        user_point = E.lift_x(x)
    except ValueError:
        print(f"Invalid point: {x} does not describe any point on the curve")
        return False
    sig_point = sig - secret_point
    # don't want to make you wait too long
    # c = sig_point.log(user_point)
    c = 0x69
    c = pow(c, e, n)
    return c == m

assert curve_p.bit_length() == 513
assert order.bit_length() == 513

K = GF(curve_p)
a = K(a)
b = K(b)
K = GF(curve_p)
E = EllipticCurve(K, (a, b))
E.set_order(order)
secret_point = E(secret_point_x, secret_point_y)

flag = int.from_bytes(FLAG, byteorder='big')

p = random_prime(2<<255, lbound=2<<254)
q = random_prime(2<<255, lbound=2<<254)
n = p*q

while flag >= n or n>curve_p or n>order:
    p = random_prime(2<<255, lbound=2<<254)
    q = random_prime(2<<255, lbound=2<<254)
    n = p*q 

e = 0x10001
d = pow(e, -1, (p-1)*(q-1))

print("Welcome to my custom signing and verification system!")
print("Here are my public parameters:")
print(f"e: {e}")
print(f"n: {n}")

print(f"Leak: {pow(flag, e, n)}")

while True:
    print("1. Sign\n2. Verify\n3. Exit")
    choice = int(input())
    if choice == 1:
        m = int(input("Enter message: "))
        x = Integer(input("Enter x-coordinate of your point: "))
        sig = sign(m, x)
        print(f"Signature: {sig}")
    elif choice == 2:
        try:
            sig_x = Integer(input("Enter x-coordinate of signature: "))
            sig_y = Integer(input("Enter y-coordinate of signature: "))
            sig = E(sig_x, sig_y)
        except TypeError:
            print("Invalid signature")
            continue
        m = int(input("Enter message: "))
        x = K(Integer(input("Enter x-coordinate of your point: ")))
        if verify(sig, m, x):
            print("Valid signature")
        else:
            print("Invalid signature")
    elif choice == 3:
        break
    else:
        print("Invalid choice")
