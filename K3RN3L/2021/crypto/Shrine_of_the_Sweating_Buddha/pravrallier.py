#!/usr/bin/env python3
#
# Polymero
#

# Imports
import random
from Crypto.Util.number import GCD, inverse, bytes_to_long, long_to_bytes, getPrime
from time import sleep


class Pravrallier:
    def __init__(self):
        # Keygen
        while True:
            p, q = getPrime(512), getPrime(512)
            if GCD(p*q, (p-1)*(q-1)) == 1:
                break
        self.n = p * q
        # Blinding
        self.r = { r+1 : random.randint(2, self.n-1) for r in range(128) }
        self.i = 1

    def fortune(self, msg):
        """ Generate fortune ticket flavour text. """
        nums = [int.from_bytes(msg[i:i+2],'big') for i in range(0,len(msg),2)]
        luck = ['']
        spce = b'\x30\x00'.decode('utf-16-be')
        for num in nums:
            if num >= 0x4e00 and num <= 0x9fd6:
                luck[-1] += num.to_bytes(2,'big').decode('utf-16-be')
            else:
                luck += ['']
        luck += ['']
        maxlen = max([len(i) for i in luck])
        for i in range(len(luck)):
            luck[i] += spce * (maxlen - len(luck[i]))
        card = [spce.join([luck[::-1][i][j] for i in range(len(luck))]) for j in range(maxlen)]
        return card

    def encrypt_worry(self, msg):
        # Generate fortune ticket
        card = self.fortune(msg)
        # Encrypt
        gm  = pow(1 + self.n, bytes_to_long(msg), self.n**2)
        rn  = pow(self.r[len(card[0])] * self.i, self.n + self.i, self.n**2)
        cip = (gm * rn) % self.n**2 
        self.i += 1
        return cip, card

    def encrypt_flag(self, msg, order, txt):
        # Generate fortune ticket
        card = self.fortune(msg)
        # Encrypt up to given order
        cip = bytes_to_long(msg)
        for o in range(2,order+1):
            cip = pow(1 + self.n, cip, self.n**(o))
            # ???
            print("|  {}".format(txt[(o-2) % len(txt)]))
            sleep(3)
        return cip, card

    def print_card(self, cip, card):
        """ Print fortune ticket to terminal. """
        upper_hex = long_to_bytes(cip).hex().upper()
        fwascii = list(''.join([(ord(i)+65248).to_bytes(2,'big').decode('utf-16-be') for i in list(upper_hex)]))
        enclst = [''.join(fwascii[i:i+len(card[0])]) for i in range(0, len(fwascii), len(card[0]))]
        # Frame elements
        sp = b'\x30\x00'.decode('utf-16-be')
        dt = b'\x30\xfb'.decode('utf-16-be')
        hl = b'\x4e\x00'.decode('utf-16-be')
        vl = b'\xff\x5c'.decode('utf-16-be')
        # Print fortune ticket
        enclst[-1] += sp*(len(card[0])-len(enclst[-1]))
        print()
        print(2*sp + dt + hl*(len(card[0])+2) + dt)
        print(2*sp + vl + dt + hl*len(card[0]) + dt + vl)
        for row in card:
            print(2*sp + 2*vl + row + 2*vl)
        print(2*sp + vl + dt + hl*len(card[0]) + dt + vl)
        for row in enclst:
            print(2*sp + vl + sp + row + sp + vl)
        print(2*sp + dt + hl*(len(card[0])+2) + dt)
        print()
