#!/usr/bin/env python3
#
# Polymero
#

# Imports
import numpy as np
import os, random, hashlib

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

NBYT = 6

class O8A:
    def __init__(self, secret):
        if len(secret) > 2*3*NBYT:
            raise ValueError('INIT ERROR -- Secret is too large, max {} bytes.'.format(2*3*NBYT))
        self.secret = secret
        while True:
            self.treasure, self.apollonii = self.bury_treasure()
            if self.apollonii:
                break
        self.points, self.shares = self.give_out_shares()
    
    def bury_treasure(self):
        secret = self.secret[::]
        distr = [len(secret) // 6 + (1 if x < len(secret) % 6 else 0)  for x in range(6)]
        C1, C2, C3 = [[secret[sum(distr[:i]):sum(distr[:i+1])] for i in range(6)][j:j+2] for j in range(0,6,2)]

        for i in range(3):
            for j in range(2):
                k = [C1,C2,C3][i][j]
                while len(k) < NBYT:
                    k += os.urandom(1)
                [C1,C2,C3][i][j] = int.from_bytes(k, 'big')

        C1 += [int.from_bytes(os.urandom(NBYT), 'big') // 4 + 2**(NBYT*8-4)]
        C2 += [int.from_bytes(os.urandom(NBYT), 'big') // 4 + 2**(NBYT*8-4)]
        C3 += [int.from_bytes(os.urandom(NBYT), 'big') // 4 + 2**(NBYT*8-4)]

        apollonii = []
        for i in range(8):
            sr1, sr2, sr3 = [(-1)**int(j) for j in list('{:03b}'.format(i))]
            
            a2 = 2 * (C1[0] - C2[0])
            b2 = 2 * (C1[1] - C2[1])
            c2 = 2 * (sr1 * C1[2] + sr2 * C2[2])
            d2 = (C1[0]**2 + C1[1]**2 - C1[2]**2) - (C2[0]**2 + C2[1]**2 - C2[2]**2)
            
            a3 = 2 * (C1[0] - C3[0])
            b3 = 2 * (C1[1] - C3[1])
            c3 = 2 * (sr1 * C1[2] + sr3 * C3[2])
            d3 = (C1[0]**2 + C1[1]**2 - C1[2]**2) - (C3[0]**2 + C3[1]**2 - C3[2]**2)
            
            AB = a2 * b3 - a3 * b2;   BA = -AB
            AC = a2 * c3 - a3 * c2;   CA = -AC
            AD = a2 * d3 - a3 * d2;   DA = -AD
            BC = b2 * c3 - b3 * c2;   CB = -BC
            BD = b2 * d3 - b3 * d2;   DB = -BD
            CD = c2 * d3 - c3 * d2;   DC = -CD
            
            ABC_a = (BC / AB)**2 + (CA / AB)**2 - 1
            ABC_b = 2 * DB * BC / (AB**2) - 2 * C1[0] * BC / AB + 2 * AD * CA / (AB**2) - 2 * C1[1] * CA / AB - 2 * sr1 * C1[2]
            ABC_c = (DB / AB)**2 - 2 * C1[0] * DB / AB + C1[0]**2 + (AD / AB)**2 - 2 * C1[1] * AD / AB + C1[1]**2 - C1[2]**2
            
            if ABC_b**2 - 4 * ABC_a * ABC_c < 0:
                return None, None
            
            ABC_r = (-ABC_b - np.sqrt(ABC_b**2 - 4 * ABC_a * ABC_c)) / (2 * ABC_a)
            
            if ABC_r < 0:
                ABC_r = (-ABC_b + np.sqrt(ABC_b**2 - 4 * ABC_a * ABC_c)) / (2 * ABC_a)
            
            r = ABC_r
            x = (DB + r * BC) / AB
            y = (AD + r * CA) / AB
            
            if np.isnan(r) or r <= 0:
                return None, None
            
            apollonii += [[round(x), round(y), round(r)]]
            
        return [C1,C2,C3], apollonii
    
    def give_out_shares(self):
        shares = []
        for C in self.apollonii:
            rnd = []
            while len(rnd) < 3:
                r = int.from_bytes(os.urandom(4),'big')
                if r not in rnd:
                    rnd += [r]
            
            shares += [
                [int(C[2] * np.cos( 2*np.pi * rnd[i]/256**4 ) + C[0]),
                 int(C[2] * np.sin( 2*np.pi * rnd[i]/256**4 ) + C[1])]
                for i in range(3)
            ]
            
        points = shares[::]
            
        for i,s in enumerate(shares):
            shares[i] = '{}.{:0{n}x}.{:0{n}x}'.format((i//3)+1,s[0],s[1], n=2*(NBYT+1))
            
        return points, shares

o8a = O8A(FLAG)
SHARES = o8a.shares

HDR = r"""|
|       ____ ____ ___  ____ ____    ____ ____    ___ _  _ ____      
|       |  | |__/ |  \ |___ |__/    |  | |___     |  |__| |___      
|       |__| |  \ |__/ |___ |  \    |__| |        |  |  | |___      
|   ____ _ ____ _  _ ___     ____ ___  ____ _    _    ____ _  _ _ _ 
|   |___ | | __ |__|  |      |__| |__] |  | |    |    |  | |\ | | | 
|   |___ | |__] |  |  |      |  | |    |__| |___ |___ |__| | \| | | 
|
|"""

print(HDR)

for _ in range(9):

    username = input("| Username: ")

    share = SHARES.pop(int(hashlib.sha256(username.encode()).hexdigest(),16) % len(SHARES))

    print("|\n| Dear {},".format(username))
    print("|  Here is your share: {}".format(share))
    print("|\n|")

print("| -- Out of 24 shares you have received 9, any more and I might just as well tell you the FLAG ---")
print("|\n|")
