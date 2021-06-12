p = 35953130875571662629774552621633952493346190947047
q = 68201352784431955275947627343562102980308744031461
n = p * q
e = 3

R = Zmod(n)
MS = MatrixSpace(R, 5, 5)
s = PermutationGroupElement('(1,4)(2,3,5)')
P = MS(s.matrix())

def encrypt(m):
	M = m * P
	return (M^e).list()
