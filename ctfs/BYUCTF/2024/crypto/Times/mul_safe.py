import hashlib
from Crypto.Cipher import AES 
from Crypto.Util.Padding import pad, unpad
from ellipticcurve import * # I'll use my own library for this
from base64 import b64encode
import os
from Crypto.Util.number import getPrime

def encrypt_flag(shared_secret: int, plaintext: str):
    iv = os.urandom(AES.block_size)

    #get AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode('ascii'))
    key = sha1.digest()[:16]

    #encrypt flag
    plaintext = pad(plaintext.encode('ascii'), AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(plaintext)

    return { "ciphertext" : b64encode(ciphertext), "iv" : b64encode(iv) }
    
def main():
    the_curve = EllipticCurve(13, 245, getPrime(128))
    start_point = None
    while start_point is None:
        x = getPrime(64)
        start_point = the_curve.point(x)
    print("Curve: ", the_curve)
    print("Point: ", start_point)
    new_point = start_point * 1337

    flag = "byuctf{REDACTED}"
    print(encrypt_flag(new_point.x, flag))

if __name__ == "__main__":
    main()
