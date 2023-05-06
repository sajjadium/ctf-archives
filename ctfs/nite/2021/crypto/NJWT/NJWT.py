import base64
from Crypto.Util.number import *
import sys
import random
import os
import sympy

class NJWT:
    n = 1
    e = 1
    d = 1

    def __init__(self):
        self.genkey()
        return

    def genkey(self):
        p = getStrongPrime(1024)
        q = p
        k = random.randint(0,100)
        for _ in range(k):
            q += random.randint(0,100)
        q = sympy.nextprime(q)
        self.n = p*q
        self.e = 17
        self.d = inverse(self.e,(p-1)*(q-1))
        return

    # Utility function to just add = to base32 to ensure right padding
    def pad(self,data):
        if len(data)%8 != 0:
            data += b"=" * (8-len(data)%8)
        return data

    def sign(self,token):
        sig = long_to_bytes(pow(bytes_to_long(token),self.d,self.n))
        return sig

    def generate_token(self,username):
        if 'admin' in username:
            print("Not authorized to generate token for this user")
            return "not_auth"

        header = b'{"alg": "notRS256", "typ": "notJWT"}'
        payload = b'{user : "' + username.encode() + b'", admin : False}'
        token = header + payload
        sig = self.sign(token)
        # Base-32 and underscores cuz its NOT JWT
        token = base64.b32encode(header).decode().strip("=") + "_" + base64.b32encode(payload).decode().strip("=") + "_" + base64.b32encode(sig).decode().strip("=")
        return token

    def verify_token(self,token):
        data = token.split("_")
        header = base64.b32decode(self.pad(data[0].encode()))
        if header != b'{"alg": "notRS256", "typ": "notJWT"}':
            return "invalid_header"

        payload = base64.b32decode(self.pad(data[1].encode()))

        if not b'admin : True' in payload:
            return "access_denied"
            
        given_sig = bytes_to_long(base64.b32decode(self.pad(data[2].encode())))
        msg = long_to_bytes(pow(given_sig,self.e,self.n))
        if msg == header+payload:
            return "Success"
        else:
            return "invalid_signature"
        return
