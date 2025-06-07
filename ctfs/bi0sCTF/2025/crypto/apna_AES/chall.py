from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from os import urandom
import json

key = urandom(16)
iv1, iv2 = urandom(16), urandom(16)

class AES_APN:
    def __init__(self):
        self.key = key

    def xor(self, a, b):
        return bytes([x^y for x,y in zip(a,b)])

    def encrypt(self, pt, iv1, iv2):
        blocks = [pt[i:i+16] for i in range(0, len(pt), 16)]
        ct = b""
        state1, state2 = iv1, iv2
        for i in range(len(blocks)):
            block = self.xor(blocks[i], state1)
            cipher = AES.new(self.key, AES.MODE_ECB)
            enc = cipher.encrypt(block)
            ct += self.xor(enc, state2)
            state2 = block
            state1 = enc
        return ct

    def decrypt(self, ct, iv1, iv2):
        blocks = [ct[i:i+16] for i in range(0, len(ct), 16)]
        pt = b""
        state1, state2 = iv1, iv2
        for i in range(len(blocks)):
            block = self.xor(blocks[i], state2)
            cipher = AES.new(self.key, AES.MODE_ECB)
            dec = cipher.decrypt(block)
            pt += self.xor(dec, state1)
            state1 = block
            state2 = dec
        try:
            unpad(pt, 16)
        except:
            return "Invalid padding"
        else:
            return "Valid padding"

def main():
    s='''
+----------------------------------------------------------+
|   ◦ APNA-AES v1.0 ◦                                      |
|   > Decryption protocol active                           |
|   > Encryption module: [offline]                         |
+----------------------------------------------------------+
'''
    print(s)
    custom = AES_APN()
    message = open("message.txt","rb").read().strip()
    enc_message = custom.encrypt(pad(message, 16), iv1, iv2)
    token = {"IV1": iv1.hex(), "IV2": iv2.hex(), "ciphertext": enc_message.hex()}
    print(f"Here is the encrypted message : {json.dumps(token)}")
    while True:
        try:
            token = json.loads(input("Enter token: "))
            ct = bytes.fromhex(token["ciphertext"])
            iv1 = bytes.fromhex(token["IV1"])
            iv2 = bytes.fromhex(token["IV2"])
            pt = custom.decrypt(ct, iv1, iv2)
            print("Decryption result: ", json.dumps({"result": pt}))
        except:
            exit(0)

if __name__ == "__main__":
    try:
        main()
    except:
        print("\nBYE")
        exit(0)
