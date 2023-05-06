from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json

flag = b'OFPPT-CTF{Not_the_real_flag}'

def gen_key(option=0):
    alphabet = b'0123456789abcdef'
    const = b'0fpptCTF5!@#'
    key = b''
    for i in range(16-len(const)):
        key += bytes([alphabet[randint(0,15)]])

    if option:
        return key + const
    else:
        return const + key

def encrypt(data, key1, key2):
    cipher = AES.new(key1, mode=AES.MODE_ECB)
    ct = cipher.encrypt(pad(data, 16))
    cipher = AES.new(key2, mode=AES.MODE_ECB)
    ct = cipher.encrypt(ct)
    return ct.hex()


def challenge():
    k1 = gen_key()
    k2 = gen_key(1)

    
    ct = encrypt(flag, k1, k2)
    
    
    print('Super strong encryption service approved by 2022 stansdards.\n'+\
                    'Message to decrypt:\n' +ct + '\nEncrypt your text:\n> ')
    try:
            
        dt = json.loads(input().strip())
        pt = bytes.fromhex(dt['pt'])
        res = encrypt(pt, k1, k2)
        print(res + '\n')
        exit(1)
    except Exception as e:
        print(e)
        print('Invalid payload.\n')
        exit(1)
    
if __name__ == "__main__":
    challenge()
