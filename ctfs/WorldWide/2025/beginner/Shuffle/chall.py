from hashlib import sha256
import os
from random import shuffle

class Cipher:
    def __init__(self):
        self.state = [i for i in range(10000)]
        shuffle(self.state)
    
    def key(self):
        shuffled = []
        for i in range(5000):
            shuffled.append(self.state[i])
            shuffled.append(self.state[5000+i])
        self.state = shuffled
        return sha256((':'.join(map(str,self.state))).encode()).digest()[0]
    
    def encrypt(self, data):
        return bytes([data[i] ^ self.key() for i in range(len(data))])
    
FLAG = os.environ['FLAG'] if 'FLAG' in os.environ else 'wwctf{example_flag}'
cipher = Cipher()
print("Welcome to my encryption service! Here's a demo!")
print(cipher.encrypt(FLAG.encode()).hex())
try:
    for i in range(10):
        text = bytes.fromhex(input(f"Input {i+1} (hex): "))
        print(cipher.encrypt(text).hex())

    print("Thank you for using my service!")
except Exception:pass
except OSError:pass