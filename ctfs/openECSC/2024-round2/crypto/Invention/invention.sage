#!/usr/bin/env sage

import os
from Crypto.Util.number import bytes_to_long
import string
import random

flag = os.getenv('FLAG', 'flag{redacted}')

debug = True

p = 0xffffffffffffffffffffffffffffffff7fffffff
N = p.bit_length()//8
F = GF(p)
a = F(0xffffffffffffffffffffffffffffffff7ffffffc)
b = F(0x1c97befc54bd7a8b65acf89f81d4d4adc565fa45)
n = 0x0100000000000000000001f4c8f927aed3ca752257
E = EllipticCurve(F, (a, b))
G = E(0x4a96b5688ef573284664698968c38bb913cbfc82, 0x23a628553168947d59dcc912042351377ac5fb32)
E.set_order(n)

d = F(1)
while d.is_square():
    d += 1

nt = 0xfffffffffffffffffffe0b3706d8512b358adda9
ET = E.quadratic_twist(d)
ET.set_order(nt)
GT = ET.gens()[0]

k1, k2 = randint(0, n-1), randint(0, nt-1)

if debug:
    print(f"[D] {k1 = }")
    print(f"[D] {k2 = }")

Pu = k1*G
PTu = k2*GT

safe_blocks = []

user_tokens = {}
user_pwds = {}

blocked_users = []

def hash_block(M, Ci, CTi):
    try:
        Pm = E.lift_x(M)
        Ci += Pm
    except:
        Pm =  ET.lift_x(M*d*4)
        CTi += Pm
    return Ci, CTi

def elliptic_hash(m, register = False):
    assert len(m) >= 2*N

    if len(m) % N != 0:
        pad_length = N - (len(m) % N)
        m += b"\x80"
        m += b"\x00"*(pad_length-1)

    m_blocks = [ZZ(bytes_to_long(m[i:i+N])) for i in range(0, len(m), N)]

    k0 = m_blocks[0]
    k1 = m_blocks[1]


    Ci = k0*Pu
    CTi = k1*PTu

    for i in range(2, len(m_blocks)):
        if register:
            safe_blocks.append(m_blocks[i])
        else:
            if m_blocks[i] not in safe_blocks:
                raise Exception("Hacking attempt detected")
        Ci, CTi = hash_block(m_blocks[i], Ci, CTi)

    return Ci, CTi

def register(user, token, pwd):
    assert pwd.decode().startswith(token)

    pwd_hash = elliptic_hash(pwd, register=True)

    user_tokens[user] = token
    user_pwds[pwd_hash] = user

    if debug:
        print(f"[D] Registered user '{user}' with token '{token}' and password '{pwd.hex()}'")


def login(user, pwd):
    if user not in blocked_users and user in user_tokens:
        token = user_tokens[user]
        pwd_hash = elliptic_hash(pwd)
        if pwd.decode().startswith(token) and pwd_hash in user_pwds:
            return user_pwds[pwd_hash]
    return None

if __name__ == "__main__":

    if debug:
        print("\n[D] Testing registration")
    user = input("Username: ")
    token = ''.join(random.choices(string.ascii_letters, k=N))
    print(f"Choose a password that starts with {token}")
    pwd = bytes.fromhex(input("Password: "))
    register(user, token, pwd)

    # Oh I forgot to register the admin!
    user = "admin"
    pwd = ''.join(random.choices(string.ascii_letters, k=N*3))
    register(user, pwd[:N], pwd.encode())

    blocked_users.append(user)


    if debug:
        print("\n[D] Testing login")
    user = input("Username: ")
    pwd = bytes.fromhex(input("Password: "))

    logged_user = login(user, pwd)

    if logged_user == "admin":
        print(f"How did you do that? You deserve a prize: {flag}")
    elif logged_user != None:
        print("It works!")
    else:
        print("Oh no, something broke :(")
