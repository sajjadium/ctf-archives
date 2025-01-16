import base64
import hashlib
import json
import os
import re
import sys
import time
from secret import FLAG


def xor(message0: bytes, message1: bytes) -> bytes:
    return bytes(byte0 & byte1 for byte0, byte1 in zip(message0, message1))


def sha256(message: bytes) -> bytes:
    return hashlib.sha256(message).digest()


def hmac_sha256(key: bytes, message: bytes) -> bytes:
    blocksize = 64
    if len(key) > blocksize:
        key = sha256(key)
    if len(key) < blocksize:
        key = key + b'\x00' * (blocksize - len(key))
    o_key_pad = xor(b'\x5c' * blocksize, key)
    i_key_pad = xor(b'\x3c' * blocksize, key)
    return sha256(o_key_pad + sha256(i_key_pad) + message)


def sha256_jwt_dumps(data: dict, exp: int, key: bytes):
    header = {'alg': 'HS256', 'typ': 'JWT'}
    payload = {'sub': data, 'exp': exp}
    header = base64.urlsafe_b64encode(json.dumps(header).encode())
    payload = base64.urlsafe_b64encode(json.dumps(payload).encode())
    signature = hmac_sha256(key, header + b'.' + payload)
    signature = base64.urlsafe_b64encode(signature).rstrip(b'=')
    return header + b'.' + payload + b'.' + signature


def sha256_jwt_loads(jwt: bytes, exp: int, key: bytes) -> dict | None:
    header_payload, signature = jwt.rsplit(b'.', 1)

    sig = hmac_sha256(key, header_payload)
    sig = base64.urlsafe_b64encode(sig).rstrip(b'=')
    if sig != signature:
        raise ValueError('JWT error')

    try:
        header, payload = header_payload.split(b'.')[0], header_payload.split(b'.')[-1]
        header = json.loads(base64.urlsafe_b64decode(header))
        payload = json.loads(base64.urlsafe_b64decode(payload))
        if (header.get('alg') != 'HS256') or (header.get('typ') != 'JWT'):
            raise ValueError('JWT error')
        if int(payload.get('exp')) < exp:
            raise ValueError('JWT error')
    except Exception:
        raise ValueError('JWT error')
    return payload.get('sub')


def register(username: str, key: bytes):
    if re.fullmatch(r'[A-z0-9]+', username) is None:
        raise ValueError("'username' format error.")
    return sha256_jwt_dumps({'username': username}, int(time.time()) + 86400, key)


def login(token: bytes, key: bytes):
    userdata = sha256_jwt_loads(token, int(time.time()), key)
    return userdata['username']


def menu():
    for _ in range(32):
        print('==================')
        print('1. Register')
        print('2. Login')
        print('3. Exit')
        try:
            choice = int(input('> '))
        except Exception:
            pass
        if 1 <= choice <= 3:
            return choice
        print('Error choice !', end='\n\n')
    sys.exit()


def main():
    key = os.urandom(32)
    for _ in range(32):
        choice = menu()
        if choice == 1:
            username = input('Username > ')
            try:
                token = register(username, key)
            except Exception:
                print('Username Error !', end='\n\n')
                continue
            print(f'Token : {token.hex()}', end='\n\n')
        if choice == 2:
            token = bytes.fromhex(input('Token > '))
            try:
                username = login(token, key)
            except Exception:
                print('Token Error !', end='\n\n')
            if username == 'Admin':
                print(f'FLAG : {FLAG}', end='\n\n')
                sys.exit()
            else:
                print('FLAG : TSC{???}', end='\n\n')
        if choice == 3:
            sys.exit()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()
