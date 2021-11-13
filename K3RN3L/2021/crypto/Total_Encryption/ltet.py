#!/usr/bin/env python3
#
# Polymero
#

# Imports
import os, time, base64
from Crypto.Util.number import getPrime, inverse, GCD, long_to_bytes

# Shorthand
def b64enc(x):
    return base64.urlsafe_b64encode(long_to_bytes(x)).rstrip(b'=')

class LTET:
    """ Layered Totally Encrypted Terminal. """
    def __init__(self, max_bit_length):
        self.maxlen = max_bit_length
        
        # Set bit lengths
        self.bitlen = {
            'inner block' : self.maxlen,
            'inner clock' : (7 * self.maxlen) // 125
        }
        self.bitlen['outer block'] = 16 + (4 * (self.bitlen['inner block'] + self.bitlen['inner clock'] + 9)) // 3
        self.bitlen['outer blind'] = 8 + (4 * self.bitlen['inner clock']) // 3
        
        # Key generation
        self.public  = { 'n' : [], 'e' : [65537, 5, 127]}
        self.private = { 'p' : [], 'q' : [], 'd' : []}
        for i in range(3):
            nbit = [self.bitlen[j] for j in ['inner clock', 'inner block', 'outer block']][i]
            while True:
                p, q = [getPrime((nbit + 1) // 2) for _ in range(2)]
                if GCD(self.public['e'][i], (p-1)*(q-1)) == 1:
                    d = inverse(self.public['e'][i], (p-1)*(q-1))
                    break
            self.private['p'] += [p]
            self.private['q'] += [q]
            self.private['d'] += [d]
            self.public['n']  += [p * q]
            
    def encrypt(self, msg):
        assert len(msg) * 8 <= self.maxlen
        clock = pow(int(time.time()), self.public['e'][0], self.public['n'][0])
        block = b64enc(pow(int.from_bytes(msg, 'big') ^ int(clock), self.public['e'][1], self.public['n'][1]))
        blind = int.from_bytes(os.urandom((self.bitlen['outer blind'] + 7) // 8), 'big') >> (8 - (self.bitlen['outer blind'] % 8))
        block = pow(int.from_bytes(block + b'.' + b64enc(clock) ,'big') ^ blind, self.public['e'][2], self.public['n'][2])
        return (b64enc(blind) + b'.' + b64enc(block)).decode()
