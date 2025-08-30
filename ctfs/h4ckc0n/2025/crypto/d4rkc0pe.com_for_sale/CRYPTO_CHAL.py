#!/usr/bin/env python3

import re
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long, long_to_bytes, getPrime
from pkcs1 import emsa_pkcs1_v15
p1 = getPrime(1024)
p2 = getPrime(1024)
N = p1 * p2
E = 0x10001
phi = (p1-1)*(p2-1)
D = pow(E,-1,N)


FLAG = b"d4rk{REDACTED}c0de"

MSG = 'hippity hoppity give my server keys as they are my properties'
DIGEST = emsa_pkcs1_v15.encode(MSG.encode(), 256)
SIGNATURE = pow(bytes_to_long(DIGEST), D, N)


class Challenge():
    def __init__(self):
        self.before_input = "This server validates domain ownership with RSA signatures. Present your message and public key, and if the signature matches ours, you must own the domain.\n"

    def challenge(self, your_input):
        if not 'option' in your_input:
            return {"error": "You must send an option to this server"}

        elif your_input['option'] == 'get_signature':
            return {
                "N": hex(N),
                "e": hex(E),
                "signature": hex(SIGNATURE)
            }

        elif your_input['option'] == 'verify':
            msg = your_input['msg']
            n = int(your_input['N'], 16)
            e = int(your_input['e'], 16)
            if e < 65537 or n%2 == 0 or n.bit_length() < 2048:
                return {"msg":"please use standard public key values"}
            digest = emsa_pkcs1_v15.encode(msg.encode(), 256)
            calculated_digest = pow(SIGNATURE, e, n)
            
            if bytes_to_long(digest) == calculated_digest:
                r = re.match(r'^I am Mallory.*own d4rkc0pe.com$', msg)
                if r:
                    return {"msg": f"Ownership switched, use the flag as default keys as ownership switches: {FLAG}"}
                else:
                    return {"msg": f"Ownership verified."}
            else:
                return {"error": "Invalid signature"}

        else:
            return {"error": "Invalid option"}
'''
upload payload in json encoded format 
{"option":"get_signature"}
{"option":"verify","msg":"<msg>","N":"<hex>","e":"<hex>"}
'''

