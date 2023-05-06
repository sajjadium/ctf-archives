from sage.all import *
import os.path

##############################################################
################ NOT NEEDED TO SOLVE THE CHAL ################
##############################################################

def is_point_on_curve(P,a,b,p):
	x = P[0]
	y = P[1]
	if ((y**2) % p == (x**3 + a*x + b) % p):
		return true
	else:
		return false


def get_s_from_x(x,a,b,p):
	"""
	s is the same as y**2
	"""
	return (x**3 + a*x + b) % p


def has_QRp(a, p):
	"""
	Euler's criterion

	x**2 = a % p -> does x exist? 
	not all a's in p have an x
	"""
	if p % 2 == 0:
		return False

	return pow(a, (p-1) >> 1, p) == 1


def get_y_from_s(s,p):
	"""
	Tonellis Algorithm
	"""

	if not has_QRp(s, p):
		return 0


	if (p % 4 == 3):
		return pow(s, (p + 1) / 4, p)

	h = 2
	while (has_QRp(h, p)):
		h += 1
	
	s_exp = (p-1) >> 1
	h_exp = p-1
	h_exp_half = (p-1) >> 1
	res = (pow(s,s_exp, p) * pow(h, h_exp, p)) % p;
	
	# finished when (s_exp is odd) and (s^s_exp * h^h_exp == 1 (mod p))
	while (s_exp % 2 == 0 or res != 1) :
	
		if (res == 1):
			s_exp = s_exp >> 1
			h_exp = h_exp >> 1

		else:
			h_exp = h_exp + h_exp_half
		
		res = (pow(s, s_exp, p) * pow(h, h_exp, p)) % p

	# pow(s, (s_exp + 1) / 2, p) * pow(h, (h_exp / 2), p)) % p;
	y = (pow(s, (s_exp + 1) >> 1, p) * pow(h, h_exp >> 1, p)) % p
	
	return y

##############################################################
################ NOT NEEDED TO SOLVE THE CHAL ################
##############################################################


# initialize the Eliptic Curve for my super safe encryption algorithm
p = 692893
a = 1
b = 6
E = EllipticCurve(GF(p),[a,b])

# initialize Alice's parameters for my super safe encryption algorithm
P = E(683798, 652629)
kA = 4001
A = P * kA
public_key_alice = (E,p,P,A)

# initialize Bob's parameters for my super safe encryption algorithm
kB = 2956
B = kB * P

m = b"<REDACTED>"

Ms = []
for M in m:
	# shift it so it has 5 new bits to find an x cordinate on the curve
	# reversible (after decryption) with M >> 5
	M = M << 5

	# find a point on the curve
	for i in range(2**5):
		x = M + i
		s = get_s_from_x(x, a, b, p)
		if has_QRp(s, p):
			y = get_y_from_s(s, p)
			Ms.append(E(x,y))
			break

	else:
		raise Exception("No point found for char: " + chr(b))

# encrypt Bob's flag for Alice
Cs = []
for M in Ms:
	C = M + kB * A
	Cs.append(str(C))

# encrypted = ['(139549 : 235923 : 1)', '(61125 : 136002 : 1)', '(260374 : 487393 : 1)', '(358186 : 437717 : 1)', '(450408 : 64836 : 1)', '(296195 : 499736 : 1)', '(636196 : 201912 : 1)', '(139817 : 13332 : 1)', '(595623 : 386881 : 1)', '(260374 : 487393 : 1)', '(47366 : 489310 : 1)', '(612562 : 56173 : 1)', '(260374 : 487393 : 1)', '(595623 : 386881 : 1)', '(139817 : 13332 : 1)', '(612562 : 56173 : 1)', '(349221 : 311135 : 1)', '(595623 : 386881 : 1)', '(218836 : 588967 : 1)', '(501307 : 184436 : 1)', '(440634 : 662065 : 1)', '(287706 : 158561 : 1)', '(318996 : 554853 : 1)']

if os.path.isfile("out.txt"):
    input("W0aH th3Re, y0U d0n'7 w4Nt T0 0veRwRite mY cIpH3r. W0n'T y0U, AlicE?")

f = open("out.txt", "w")
f.write("\n".join(Cs))
f.close()

