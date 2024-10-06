#!/usr/bin/python3

import ctypes
import requests
from getpass import getpass
from hashlib import sha256
from base64 import b64encode
from sys import exit

def generateToken(username :str, password_hash :bytes, access :int) -> bytes:
    _tokengen :CDLL = ctypes.CDLL('./tokengen.so')
    _tokengen.generateToken.argtypes :tuple[PyCSimpleType] = (ctypes.c_char_p, ctypes.c_uint16, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_uint8)
    _tokengen.generateToken.restype :PyCPointerType = ctypes.POINTER(ctypes.c_ubyte)
    _tokengen.free.argtypes :tuple[PyCSimpleType] = (ctypes.c_void_p,)

    ulen :int = len(username)
    size :int = 110 + ulen

    barray :PyCArrayType = ctypes.c_ubyte * 32
    token :LP_c_ubyte = _tokengen.generateToken(ctypes.c_char_p(username.encode()), ctypes.c_uint16(ulen), barray(*password_hash), ctypes.c_uint8(access))
    ret :bytes = b64encode(bytes(token[:size]))
    _tokengen.free(token)

    return ret

def getCreds() -> tuple[str, bytes, int]:
    print('Welcome to the Super Secure Login Shell')
    print('Enter your credentials and access level to access the flag!\n')

    while True:
        username :str = input('Username: ')

        if not username or len(username) > 256:
            print('Please ensure the username is of 1-256 characters!\n')
            continue
    
        password_hash :bytes = sha256(getpass().encode()).digest()
        access :int = int(input('Access level: '))

        if not 0 <= access <= 255:
            print('Please ensure the access level is in the range 0-255!\n')
            continue

        break

    return username, password_hash, access

def login(token: bytes):
    url = 'https://b655d7019f1498a.1nf1n1ty.team/' 
    headers = {'Content-Type': 'application/octet-stream'} 

    response = requests.post(url, data=token, headers=headers) 

    if response.status_code == 200:
        print("Login successful!")
        print("Flag: ", response.content.decode()) 
    elif response.status_code == 401:
        print("Unauthorized: Invalid credentials.")
    else:
        print(f"Error: {response.status_code}, {response.content.decode()}")
        
def main() -> int:
    username, password_hash, access = getCreds()
    token :bytes = generateToken(username, password_hash, access)

    login(token)

    return 0

if __name__ == '__main__':
    exit(main())
