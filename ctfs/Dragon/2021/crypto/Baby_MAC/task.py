#!/usr/bin/env python3
import os
try:
    from Crypto.Cipher import AES
except ImportError:
    from Cryptodome.Cipher import AES

def split_by(data, cnt):
    return [data[i : i+cnt] for i in range(0, len(data), cnt)]

def pad(data, bsize):
    b = bsize - len(data) % bsize
    return data + bytes([b] * b)

def xor(a, b):
    return bytes(aa ^ bb for aa, bb in zip(a, b))

def sign(data, key):
    data = pad(data, 16)
    blocks = split_by(data, 16)
    mac = b'\0' * 16
    aes = AES.new(key, AES.MODE_ECB)
    for block in blocks:
        mac = xor(mac, block)
        mac = aes.encrypt(mac)
    mac = aes.encrypt(mac)
    return mac

def verify(data, key):
    if len(data) < 16:
        return False, ''
    tag, data = data[:16], data[16:]
    correct_tag = sign(data, key)
    if tag != correct_tag:
        return False, ''
    return True, data

def main():
    key = os.urandom(16)
    while True:
        print('What to do?')
        opt = input('> ').strip()
        if opt == 'sign':
            data = input('> ').strip()
            data = bytes.fromhex(data)
            if b'gimme flag' in data:
                print('That\'s not gonna happen')
                break
            print((sign(data, key) + data).hex())
        elif opt == 'verify':
            data = input('> ').strip()
            data = bytes.fromhex(data)
            ok, data = verify(data, key)
            if ok:
                if b'gimme flag' in data:
                    with open('flag.txt', 'r') as f:
                        print(f.read())
                else:
                    print('looks ok!')
            else:
                print('hacker detected!')
        else:
            print('??')
            break
    return 0

if __name__ == '__main__':
    exit(main())
