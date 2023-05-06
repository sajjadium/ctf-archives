import numpy as np
import requests
from binascii import hexlify

url = 'http://fine-fine.donjon-ctf.io:6000'

def send_getpubkey(data):
    cmd = {'cmd' : 'getpubkey', 'data': data }
    x = requests.post(url, json = cmd)
    if x.headers["content-type"] == "application/octet-stream":
        trace = np.frombuffer(x.content, dtype=np.uint16)
        return trace 
    else:
        return x.json()

if __name__ == "__main__":
    print(send_getpubkey("aa"*64))
    r = send_getpubkey("6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c2964fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5") # this is secp256r1's basepoint 
