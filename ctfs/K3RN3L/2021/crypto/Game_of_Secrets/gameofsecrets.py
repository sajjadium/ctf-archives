#!/usr/bin/env python3
#
# Polymero
#

# Imports
import os, base64
from hashlib import sha256

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

class GoS:
    def __init__(self, key=None, spacing=12):
        self.spacing = spacing
        if type(key) == str:
            try:    key = bytes.fromhex(key)
            except: key = None
        if (key is None) or (len(key) != 8) or (type(key) != bytes):
            key = os.urandom(8)
        self.RKs = [ sha256(key).hexdigest()[i:i+16] for i in range(0,256//4,16) ]
        self.ratchet()
        self.state = self.slicer(self.RKs[0])
        self.i = 0
    
    def slicer(self, inp):
        if type(inp) == str:
            inp = bytes.fromhex(inp)
        return [ [ int(i) for i in list('{:08b}'.format(j)) ] for j in inp ]
    
    def ratchet(self):
        self.RKs = [ sha256(rk.encode()).hexdigest()[:16] for rk in self.RKs ]
    
    def update(self):
        rk_plane = self.slicer( self.RKs[ (self.i // self.spacing) % 4 ] )
        for yi in range(8):
            for xi in range(8):
                self.state[yi][xi] = self.state[yi][xi] ^ rk_plane[yi][xi]
                
    def get_sum(self, x, y):
        ret =  [ self.state[(y-1) % 8][i % 8] for i in [x-1, x, x+1] ]
        ret += [ self.state[ y    % 8][i % 8] for i in [x-1,    x+1] ]
        ret += [ self.state[(y+1) % 8][i % 8] for i in [x-1, x, x+1] ]
        return sum(ret)
    
    def rule(self, ownval, neighsum):
        if ( neighsum < 2 ) or ( neighsum > 3 ):
            return 0
        return 1
        if neighsum == 3:
            return 1
        return ownval
    
    def tick(self):
        new_state = [ [ 0 for _ in range(8) ] for _ in range(8) ]
        for yi in range(8):
            for xi in range(8):
                new_state[yi][xi] = self.rule( self.state[yi][xi], self.get_sum(xi, yi) )
        self.state = new_state
        self.i += 1
        if (self.i % (4 * self.spacing)) == 0:
            self.ratchet()
        if (self.i % self.spacing) == 0:
            self.update()
        
    def output(self):
        return bytes([int(''.join([str(j) for j in i]),2) for i in self.state]).hex()
                
    def stream(self, nbyt):
        lst = ''
        for _1 in range(-(-nbyt//8)):
            for _2 in range(3):
                for _3 in range(self.spacing):
                    self.tick()
            lst += self.output()
        return ''.join(lst[:2*nbyt])
    
    def xorstream(self, msgcip):
        if type(msgcip) == str:
            msgcip = bytes.fromhex(msgcip)
        keystream = list(bytes.fromhex(self.stream(len(msgcip))))
        bytstream = list(msgcip)
        return bytes([ bytstream[i] ^ keystream[i] for i in range(len(msgcip)) ]).hex()


def __main__():

    gos = GoS()

    print("\n -- Here's your free stream to prepare you for your upcoming game! --\n")
    print(base64.urlsafe_b64encode(bytes.fromhex(gos.stream(1200*8))).decode())
    print('\n -- They are indistinguishable from noise, they are of variable length, and they are the key to your victory.')
    print('    Ladies and Gentlemen, give it up for THE ENCRYPTED PADDED FLAG!!! --\n')
    print(base64.urlsafe_b64encode(bytes.fromhex(
                         gos.xorstream( 
                         os.urandom(int(os.urandom(1).hex(),16)+8) +
                         FLAG +
                         os.urandom(int(os.urandom(1).hex(),16)+8) 
                         ))).decode().rstrip('='))
    print('\nGood Luck! ~^w^~\n')

__main__()
    