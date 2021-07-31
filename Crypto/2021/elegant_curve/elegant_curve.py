#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
from flag import flag

def tonelli_shanks(n, p):
    if pow(n, int((p-1)//2), p) == 1:
            s = 1
            q = int((p-1)//2)
            while True:
                if q % 2 == 0:
                    q = q // 2
                    s += 1
                else:
                    break
            if s == 1:
                r1 = pow(n, int((p+1)//4), p)
                r2 = p - r1
                return r1, r2
            else:
                z = 2
                while True:
                    if pow(z, int((p-1)//2), p) == p - 1:
                        c = pow(z, q, p)
                        break
                    else:
                        z += 1
                r = pow(n, int((q+1)//2), p)
                t = pow(n, q, p)
                m = s
                while True:
                    if t == 1:
                        r1 = r
                        r2 = p - r1
                        return r1, r2
                    else:
                        i = 1
                        while True:
                            if pow(t, 2**i, p) == 1:
                                break
                            else:
                                i += 1
                        b = pow(c, 2**(m-i-1), p)
                        r = r * b % p
                        t = t * b ** 2 % p
                        c = b ** 2 % p
                        m = i
    else:
        return False

def add(A, B, p):
	if A == 0:
		return B
	if B == 0:
		return A
	l = ((B[1] - A[1]) * inverse(B[0] - A[0], p)) % p
	x = (l*l - A[0] - B[0]) % p
	y = (l*(A[0] - x) - A[1]) % p
	return (int(x), int(y))

def double(G, a, p):
	if G == 0:
		return G
	l = ((3*G[0]*G[0] + a) * inverse(2*G[1], p)) % p
	x = (l*l - 2*G[0]) % p
	y = (l*(G[0] - x) - G[1]) % p
	return (int(x), int(y))

def multiply(point, exponent, a, p):
	r0 = 0
	r1 = point
	for i in bin(exponent)[2:]:
		if i == '0':
			r1 = add(r0, r1, p)
			r0 = double(r0, a, p)
		else:
			r0 = add(r0, r1, p)
			r1 = double(r1, a, p)
	return r0

def random_point(a, b, p):
	while True:
		x = getRandomRange(1, p-1)
		try:
			y, _ = tonelli_shanks((x**3 + a*x + b) % p, p)
			return (x, y)
		except:
			continue

def die(*args):
	pr(*args)
	quit()

def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()

def sc():
	return sys.stdin.readline().strip()

def main():
	border = "+"
	pr(border*72)
	pr(border, " hi talented cryptographers, the mission is decrypt a secret message", border)
	pr(border, " with given parameters for two elliptic curve, so be genius and send", border)
	pr(border, " suitable parameters, now try to get the flag!                      ", border)
	pr(border*72)

	nbit = 160

	while True:
		pr("| Options: \n|\t[S]end ECC parameters and solve the task \n|\t[Q]uit")
		ans = sc().lower()
		if ans == 's':
			pr("| Send the parameters of first ECC y^2 = x^3 + ax + b like: a, b, p ")
			params = sc()
			try:
				a, b, p = params.split(',')
				a, b, p = int(a), int(b), int(p)
			except:
				die("| your parameters are not valid!!")
			if isPrime(p) and 0 < a < p and 0 < b < p and p.bit_length() == nbit:
				pr("| Send the parameters of second ECC y^2 = x^3 + cx + d like: c, d, q ")
				pr("| such that 0 < q - p <= 2022")
				params = sc()
				try:
					c, d, q = params.split(',')
					c, d, q = int(c), int(d), int(q)
				except:
					die("| your parameters are not valid!!")
				if isPrime(q) and 0 < c < q and 0 < d < q and 0 < q - p <= 2022 and q.bit_length() == nbit:
					G, H = random_point(a, b, p), random_point(c, d, q)
					r, s = [getRandomRange(1, p-1) for _ in range(2)]
					pr(f"| G is on first  ECC and G =", {G})
					pr(f"| H is on second ECC and H =", {H})
					U = multiply(G, r, a, p)
					V = multiply(H, s, c, q)
					pr(f"| r * G =", {U})
					pr(f"| s * H =", {V})
					pr("| Send r, s to get the flag: ")
					rs = sc()
					try:
						u, v = rs.split(',')
						u, v = int(u), int(v)
					except:
						die("| invalid input, bye!")
					if u == r and v == s:
						die("| You got the flag:", flag)
					else:
						die("| the answer is not correct, bye!")
				else:
					die("| invalid parameters, bye!")
			else:
				die("| invalid parameters, bye!")
		elif ans == 'q':
			die("Quitting ...")
		else:
			die("Bye ...")

if __name__ == '__main__':
	main()