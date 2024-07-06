#!/usr/bin/env python3

from Crypto.Cipher import AES
import os

KEY = os.urandom(16)
IV = os.urandom(16)
FLAG = os.getenv('FLAG', 'DUCTF{testflag}')

def main():
    while True:
        ct = bytes.fromhex(input('ct: '))
        aes = AES.new(KEY, AES.MODE_CFB, IV, segment_size=128)
        try:
            print(eval(aes.decrypt(ct)))
        except Exception:
            print('invalid ct!')

if __name__ == '__main__':
    main()
