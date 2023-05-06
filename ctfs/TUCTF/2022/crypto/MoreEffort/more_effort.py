#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 22:26:57 2022

@author: weiping
"""

import os
import random
from Crypto.Util.number import *
import gmpy2

flag = b'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

class RSA():
	def __init__(self):
		self.p = getPrime(512)
		self.s = 0
		for i in range(1, 18000000):
			self.s += pow(i, self.p-2, self.p)
		self.s = self.s % self.p
		self.q = gmpy2.next_prime(self.s)
		self.n = self.p * self.q
		self.phi = (self.p - 1) * (self.q - 1)
		self.e = 65537
		self.d = pow(self.e, -1, self.phi)

	def encrypt(self, m: int):
		return pow(m, self.e, self.n)


def main():
    rsa = RSA()
    print(f"p = {rsa.p}")
    print(f"e = {rsa.e}")
    c = rsa.encrypt(bytes_to_long(flag))
    print('c = ', c)
    '''
    p = 11545307730112922786664290405312669819594345207377186481347514368962838475959085036399074594822885814719354871659183685801279739518405830244888530641898849
    e = 65537
    c =  114894293598203268417380013863687165686775727976061560608696207173455730179934925684529986102237419507146768083815607566149240438056135058988227916482404733131796310418493418060300571541865427288945087911872630289527954636816219365941817260989104786329938318143577075200571833575709614521758701838099810751
    '''
    

if __name__ == "__main__":
	main()