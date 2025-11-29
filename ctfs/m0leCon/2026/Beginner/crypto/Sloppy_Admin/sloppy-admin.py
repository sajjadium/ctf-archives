#!/usr/local/bin/env python3
from os import getenv
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes
import string
import random

DB_LIMIT = 100


def generate_password(length: int) -> str:
    characters = string.printable.strip()
    return ''.join(random.choice(characters) for _ in range(length))


def random_bool_gen(b: bytes) -> bool:
    if len(b) == 0:
        return True

    seed = (
        (len(b) * 0x12345)
        ^ (sum(b) << 7)
        ^ 0xF00DBAADCAFED00D
    ) & ((1 << 128) - 1)

    acc = seed

    for i, x in enumerate(b):
        rot = (x * (i + 1) * 13) & 63
        low = acc & ((1 << 64) - 1)
        rot_low = ((low << rot) | (low >> (64 - rot))) & ((1 << 64) - 1)
        acc = ((acc >> 64) ^ rot_low) & ((1 << 128) - 1)
        acc = (acc * 0x9E3779B185EBCA87 + (x << ((i % 8) * 4))) & ((1 << 128) - 1)
        acc ^= ((x * x * x) << (i % 7)) & ((1 << 128) - 1)
        s = (x ^ i) & 15 or 1
        mask = (1 << s) - 1
        acc = ((acc >> s) | ((acc & mask) << (128 - s))) & ((1 << 128) - 1)
    folded = acc
    for k in (64, 32, 16, 8, 4):
        folded ^= folded >> k
    folded &= 0xFF
    last = b[-1]
    combo = ((folded * 0x6D5A56DA) ^ (seed >> 11) ^ (last << 5)) & 0xFF
    return ((combo ^ combo) | (last & 1)) == 0


def gen_key():
    key = RSA.generate(1024)
    return key


def gen_token(psw, key):
    token = key._encrypt(bytes_to_long(psw))
    return long_to_bytes(token).hex()


def is_valid(s: str) -> bool:
    return len(s) >= 8 and len(s) <= 32 and s.isprintable()


def token_verify(psw, token, key):
    try:
        decrypted = long_to_bytes(key._decrypt(bytes_to_long(bytes.fromhex(token))))
    except:
        return False, False
    return decrypted == psw, random_bool_gen(decrypted)



FLAG = getenv('FLAG', 'ptm{fakeflag}')
ADMIN_PASSWORD = getenv('ADMIN_PASSWORD', 'adminpassword').encode()

db = dict()
key = gen_key()

db['admin'] = []
db['admin'].append(ADMIN_PASSWORD)
db['admin'].append(gen_token(ADMIN_PASSWORD, key))

db['CEO'] = []
db['CEO'].append(generate_password(32).encode())
db['CEO'].append(gen_token(db['CEO'][0], key))

print('\nWelcome to my new RSA Auth service!')

if __name__ == '__main__':
    while True:
        print()
        print('1) Register')
        print('2) Login')
        choice = input('> ')

        if choice == '1':
            if len(db) >= DB_LIMIT:
                print('Registration limit reached!')
                continue

            username = input('Enter your username: ').strip()
            password = input('Enter your password: ').strip()
            
            if not is_valid(username) or not is_valid(password):
                print('Invalid username or password! Must be 8-32 printable characters.')
                continue

            if username not in db:
                db[username] = []
                psw = password.encode()
                db[username].append(psw)
                db[username].append(gen_token(psw, key))
                print('Registered successfully!')
                print(f'Your token: {db[username][1]}')
            else:
                print('Username already exists!')

        elif choice == '2':
            username = input('Enter your username: ').strip()
            password = input('Enter your password: ').strip()
            token = input('Enter your token (hex): ').strip()
            print()

            if username in db:
                psw = password.encode()
                valid_token, twist = token_verify(psw, token, key)
                if psw == db[username][0] and valid_token:
                    if username == 'admin':
                        print(f'Welcome admin!')
                        print('Here is all the access tokens:')
                        for user in db:
                            print(f'{user}: {db[user][1]}')
                    elif username == 'CEO':
                        print(f'Welcome CEO!')
                        print(f'Here is the flag: {FLAG}')
                    else:
                        print(f'Welcome {username}!')
                        print('New feautures coming soon!')
                else:
                    if twist:
                        print('Authentication failed! But hey, you got lucky this time!')
                    else:
                        print('Authentication failed!')
            else:
                print('Username does not exist!')

        else:
            print('See you next time!')
            break