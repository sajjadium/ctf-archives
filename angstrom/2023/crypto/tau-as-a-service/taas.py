#!/usr/local/bin/python

from blspy import PrivateKey as Scalar

# order of curve
n = 0x73EDA753299D7D483339D80809A1D80553BDA402FFFE5BFEFFFFFFFF00000001

with open('flag.txt', 'rb') as f:
	tau = int.from_bytes(f.read().strip(), 'big')
	assert tau < n

while True:
	d = int(input('gimme the power: '))
	assert 0 < d < n
	B = Scalar.from_bytes(pow(tau, d, n).to_bytes(32, 'big')).get_g1()
	print(B)
