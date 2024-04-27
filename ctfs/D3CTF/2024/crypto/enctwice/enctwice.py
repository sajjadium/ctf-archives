import os
import secret
from random import seed, choice
from Crypto.Cipher import ChaCha20,AES
from Crypto.Util.number import *
from string import ascii_letters, digits
from hashlib import sha256

D3 = 300

def proof_of_work():
    seed(os.urandom(8))
    proof = ''.join([choice(ascii_letters + digits) for _ in range(20)])
    digest = sha256(proof.encode('latin-1')).hexdigest()
    print('sha256(XXXX + {}) == {}'.format(proof[4:], digest))
    msg = input('Give me XXXX >')
    if msg != proof[:4]:
        return False
    return True

def pad(msg):
    need = (0x20) - (len(msg) & (0x1F))
    return msg + bytes([need]) * need

def unpad(msg):
    need = msg[-1]
    for i in msg[-need:]:
        assert i == need
    return msg[:-need]

class MYENC:
    def __init__(self):
        self.CHACHA_KEY = os.urandom(32)
        self.AUTH_DATA = os.urandom(32)
        self.AES_KEY = os.urandom(32)
        self.P = getPrime(256)
        self.LIMIT = 2**250
        self.X = getPrime(251)
        self.LEGAL = "0123456789ABCDEF"
    
    def hash(self, r, s, ct):
        L = self.AUTH_DATA + ct + long_to_bytes(len(self.AUTH_DATA), 16) + long_to_bytes(len(ct), 16)
        res = 0
        for i in range(0, len(L), 32):
            res = (res + bytes_to_long(L[i:i+32]) + 2**256) * r % self.P
        return (res + s) % self.LIMIT
    
    def encrypt1(self, msg):
        msg = pad(msg)
        nonce = os.urandom(12)
        cipher = ChaCha20.new(key = self.CHACHA_KEY, nonce = nonce)
        ct = cipher.encrypt(bytes([0]) * 32 + msg)
        r, s, ct = bytes_to_long(ct[:16]), bytes_to_long(ct[16:32]), ct[32:]
        tag = self.hash(r, s, ct)
        return ct, tag, nonce
        
    def encrypt2(self, msg):
        msg = pad(msg)
        iv = os.urandom(16)
        cipher = AES.new(key = self.AES_KEY, mode = AES.MODE_OFB, iv = iv)
        ct = cipher.encrypt(msg)
        return ct, iv
    
    def encrypt_msg(self, msg):
        assert len(msg) < 32
        ct1, tag, nonce = self.encrypt1(msg)
        ct2, iv = self.encrypt2(msg)
        return ct1 + long_to_bytes(tag + bytes_to_long(ct2) * self.X) + iv + nonce
    
    def decrypt1(self, msg, tag, nonce):
        cipher = ChaCha20.new(key = self.CHACHA_KEY, nonce = nonce)
        pt = cipher.decrypt(bytes([0]) * 32 + msg)
        r, s, pt = bytes_to_long(pt[:16]), bytes_to_long(pt[16:32]), pt[32:]
        assert tag == self.hash(r, s, msg)
        return unpad(pt)
    
    def decrypt2(self, msg, iv):
        cipher = AES.new(key = self.AES_KEY, mode = AES.MODE_OFB, iv = iv)
        pt = cipher.decrypt(msg)
        return unpad(pt)
    
    def verify_msg(self, msg):
        ct1, val, iv, nonce = msg[:32], bytes_to_long(msg[32:-28]), msg[-28:-12], msg[-12:]
        tag, ct2 = val % self.X, long_to_bytes(val // self.X)
        pt1 = self.decrypt1(ct1, tag, nonce)
        pt2 = self.decrypt2(ct2, iv)
        for i, j in zip(pt1, pt2):
            assert i == j
        return "Valid message!"
    
    def change_X(self, msg):
        for i in msg:
            assert  i in self.LEGAL
        try:
            new_X = eval(msg)
        except:
            new_X = eval("0x" + msg)
        new_X = getPrime(new_X)
        if new_X < self.LIMIT:
            return  "Invalid X!"
        self.X = new_X
        return "Valid X!"

if __name__ == "__main__":
    
    if not proof_of_work():
        exit()
    
    myenc = MYENC()
    
    cnt = 7
    print(f"Now, you have {cnt} chances to modify the encryption or encrypt your own message.")
    print(f"Good luck!")
    
    for i in range(cnt):
        type = input("> ")
        if "encrypt" in type :
            try:
                msg = bytes.fromhex(input("input your message >").replace(" ","").strip())[:31]
                res = myenc.encrypt_msg(msg)
                print(res.hex())
            except:
                print("Invalid message!")
        
        elif "change X" in type :
            try:
                msg = input("input your X >")[:2]
                res = myenc.change_X(msg)
                print(res)
            except:
                print("Invalid X!")
    
    flag = secret.flag
    enc_flag = myenc.encrypt_msg(flag)
    print(f"Here is your flag:")
    print(enc_flag.hex())
    
    print(f"Now, feel free to verify your encrypted message!")
    
    while(True):
        msg = input(">")
        if msg == "exit" :
            break
        try:
            msg = bytes.fromhex(msg.replace(" ","").strip())
            res = myenc.verify_msg(msg)
            print(res)
        except:
            print("Invalid message!")
