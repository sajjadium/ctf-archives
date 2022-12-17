import math
import hashlib
from Crypto.Cipher import AES

ENC_MSG = open('msg.enc', 'rb').read()
NUM_HASH = "636e276981116cf433ac4c60ba9b355b6377a50e"

def f(i):
    if i < 5:
        return i+1
    
    return 1905846624*f(i-5) - 133141548*f(i-4) + 3715204*f(i-3) - 51759*f(i-2) + 360*f(i-1)

# Decrypt the flag
def decrypt_flag(sol):
    sol = sol % pow(10,31337)
    sol = str(sol)
    num_hash = hashlib.sha1(sol.encode()).hexdigest()
    key = hashlib.sha256(sol.encode()).digest()

    if num_hash != NUM_HASH:
        print('number not computed correctly')
        exit()

    iv = b'\x00'*16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    print(len(unpad(ENC_MSG)))
    msg_dec = cipher.decrypt(ENC_MSG)
    print(msg_dec)

if __name__ == "__main__":
    ret = f(13371337)
    decrypt_flag(ret)

