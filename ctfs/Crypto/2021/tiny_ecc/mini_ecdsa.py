#Elliptic curve basics, tools for finding rational points, and ECDSA implementation.
#Brendan Cordy, 2015

from fractions import Fraction
from math import ceil, sqrt
from random import SystemRandom, randrange
from hashlib import sha256
from time import time

#Useful constant. The order of the subgroup defined in the secp256k1 standard.

secp256k1_order = 115792089237316195423570985008687907852837564279074904382605163141518161494337

#Affine Point (+Infinity) on an Elliptic Curve ---------------------------------------------------

class Point(object):
    #Construct a point with two given coordindates.
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.inf = False

    #Construct the point at infinity.
    @classmethod
    def atInfinity(cls):
        P = cls(0, 0)
        P.inf = True
        return P

    #The secp256k1 generator.
    @classmethod
    def secp256k1(cls):
        return cls(55066263022277343669578718895168534326250603453777594175500187360389116729240,
                   32670510020758816978083085130507043184471273380659243275938904335757337482424)

    def __str__(self):
        if self.inf:
            return 'Inf'
        else:
            return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __eq__(self,other):
        if self.inf:
            return other.inf
        elif other.inf:
            return self.inf
        else:
            return self.x == other.x and self.y == other.y

    def is_infinite(self):
        return self.inf

#Elliptic Curves over any Field ------------------------------------------------------------------

class Curve(object):
    #Set attributes of a general Weierstrass cubic y^2 = x^3 + ax^2 + bx + c over any field.
    def __init__(self, a, b, c, char, exp):
        self.a, self.b, self.c = a, b, c
        self.char, self.exp = char, exp
        print(self)

    def __str__(self):
        #Cases for 0, 1, -1, and general coefficients in the x^2 term.
        if self.a == 0:
            aTerm = ''
        elif self.a == 1:
            aTerm = ' + x^2'
        elif self.a == -1:
            aTerm = ' - x^2'
        elif self.a < 0:
            aTerm = " - " + str(-self.a) + 'x^2'
        else:
            aTerm = " + " + str(self.a) + 'x^2'
        #Cases for 0, 1, -1, and general coefficients in the x term.
        if self.b == 0:
            bTerm = ''
        elif self.b == 1:
            bTerm = ' + x'
        elif self.b == -1:
            bTerm = ' - x'
        elif self.b < 0:
            bTerm = " - " + str(-self.b) + 'x'
        else:
            bTerm = " + " + str(self.b) + 'x'
        #Cases for 0, 1, -1, and general coefficients in the constant term.
        if self.c == 0:
            cTerm = ''
        elif self.c < 0:
            cTerm = " - " + str(-self.c)
        else:
            cTerm = " + " + str(self.c)
        #Write out the nicely formatted Weierstrass equation.
        self.eq = 'y^2 = x^3' + aTerm + bTerm + cTerm
        #Print prettily.
        if self.char == 0:
            return self.eq + ' over Q'
        elif self.exp == 1:
            return self.eq + ' over ' + 'F_' + str(self.char)
        else:
            return self.eq + ' over ' + 'F_' + str(self.char) + '^' + str(self.exp)

    #Compute the discriminant.
    def discriminant(self):
        a, b, c = self.a, self.b, self.c
        return -4*a*a*a*c + a*a*b*b + 18*a*b*c - 4*b*b*b - 27*c*c

    #Compute the order of a point on the curve.
    def order(self, P):
        Q = P
        orderP = 1
        #Add P to Q repeatedly until obtaining the identity (point at infinity).
        while not Q.is_infinite():
            Q = self.add(P,Q)
            orderP += 1
        return orderP

    #List all multiples of a point on the curve.
    def generate(self, P):
        Q = P
        orbit = [str(Point.atInfinity())]
        #Repeatedly add P to Q, appending each (pretty printed) result.
        while not Q.is_infinite():
            orbit.append(str(Q))
            Q = self.add(P,Q)
        return orbit

    #Double a point on the curve.
    def double(self, P):
        return self.add(P,P)

    #Add P to itself k times.
    def mult(self, P, k):
        if P.is_infinite():
            return P
        elif k == 0:
            return Point.atInfinity()
        elif k < 0:
            return self.mult(self.invert(P), -k)
        else:
            #Convert k to a bitstring and use peasant multiplication to compute the product quickly.
            b = bin(k)[2:]
            return self.repeat_additions(P, b, 1)

    #Add efficiently by repeatedly doubling the given point, and adding the result to a running
    #total when, after the ith doubling, the ith digit in the bitstring b is a one.
    def repeat_additions(self, P, b, n):
        if b == '0':
            return Point.atInfinity()
        elif b == '1':
            return P
        elif b[-1] == '0':
            return self.repeat_additions(self.double(P), b[:-1], n+1)
        elif b[-1] == '1':
            return self.add(P, self.repeat_additions(self.double(P), b[:-1], n+1))

    #Returns a pretty printed list of points.
    def show_points(self):
        return [str(P) for P in self.get_points()]

#Elliptic Curves over Q --------------------------------------------------------------------------

class CurveOverQ(Curve):
    #Construct a Weierstrass cubic y^2 = x^3 + ax^2 + bx + c over Q.
    def __init__(self, a, b, c):
        Curve.__init__(self, a, b, c, 0, 0)

    def contains(self, P):
        if P.is_infinite():
            return True
        else:
            return P.y*P.y == P.x*P.x*P.x + self.a*P.x*P.x + self.b*P.x + self.c

    def get_points(self):
        #Start with the point at infinity.
        points = [Point.atInfinity()]
        #The only possible y values are divisors of the discriminant.
        for y in divisors(self.discriminant()):
            #Each possible y value yields a monic cubic polynomial in x, whose roots
            #must divide the constant term.
            const_term = self.c - y*y
            if const_term != 0:
                for x in divisors(const_term):
                    P = Point(x,y)
                    if 0 == x*x*x + self.a*x*x + self.b*x + const_term and self.has_finite_order(P):
                        points.append(P)
            #If the constant term is zero, factor out x and look for rational roots
            #of the resulting quadratic polynomial. Any such roots must divide b.
            elif self.b != 0:
                for x in divisors(self.b):
                    P = Point(x,y)
                    if 0 == x*x*x+self.a*x*x+self.b*x+const_term and self.has_finite_order(P):
                        points.append(P)
            #If the constant term and b are both zero, factor out x^2 and look for rational
            #roots of the resulting linear polynomial. Any such roots must divide a.
            elif self.a != 0:
                 for x in divisors(self.a):
                    P = Point(x,y)
                    if 0 == x*x*x+self.a*x*x+self.b*x+const_term and self.has_finite_order(P):
                        points.append(P)
            #If the constant term, b, and a are all zero, we have 0 = x^3 + c - y^2 with
            #const_term = c - y^2 = 0, so (0,y) is a point on the curve.
            else:
                points.append(Point(0,y))
        #Ensure that there are no duplicates in our list of points.
        unique_points = []
        for P in points:
            addP = True
            for Q in unique_points:
                if P == Q:
                    addP = False
            if addP:
                unique_points.append(P)
        return unique_points

    def invert(self, P):
        if P.is_infinite():
            return P
        else:
            return Point(P.x, -P.y)

    def add(self, P_1, P_2):
        #Compute the differences in the coordinates.
        y_diff = P_2.y - P_1.y
        x_diff = P_2.x - P_1.x
        #Cases involving the point at infinity.
        if P_1.is_infinite():
            return P_2
        elif P_2.is_infinite():
            return P_1
        #Case for adding an affine point to its inverse.
        elif x_diff == 0 and y_diff != 0:
            return Point.atInfinity()
        #Case for adding an affine point to itself.
        elif x_diff == 0 and y_diff == 0:
            #If the point is on the x-axis, there's a vertical tangent there (assuming
            #the curve in nonsingular) so we obtain the point at infinity.
            if P_1.y == 0:
                return Point.atInfinity()
            #Otherwise the result is an affine point on the curve we can arrive at by
            #following the tangent line, whose slope is given below.
            else:
                ld = Fraction(3*P_1.x*P_1.x + 2*self.a*P_1.x + self.b, 2*P_1.y)
        #Case for adding two distinct affine points, where we compute the slope of
        #the secant line through the two points.
        else:
            ld = Fraction(y_diff, x_diff)
        #Use the slope of the tangent line or secant line to compute the result.
        nu = P_1.y - ld*P_1.x
        x = ld*ld - self.a  -P_1.x - P_2.x
        y = -ld*x - nu
        return Point(x,y)

    #Use the Nagell-Lutz Theorem and Mazur's Theorem to potentially save time.
    def order(self, P):
        Q = P
        orderP = 1
        #Add P to Q repeatedly until obtaining the point at infinity.
        while not Q.is_infinite():
            Q = self.add(P,Q)
            orderP += 1
            #If we ever obtain non integer coordinates, the point has infinite order.
            if Q.x != int(Q.x) or Q.y != int(Q.y):
                return -1
            #Moreover, all finite order points have order at most 12.
            if orderP > 12:
                return -1
        return orderP

    def has_finite_order(self, P):
            return not self.order(P) == -1

    def torsion_group(self):
        highest_order = 1
        #Find the rational point with the highest order.
        for P in self.get_points():
            if self.order(P) > highest_order:
                highest_order = self.order(P)
        #If this point generates the entire torsion group, the torsion group is cyclic.
        if highest_order == len(self.get_points()):
            print('Z/' + str(highest_order) + 'Z')
        #If not, by Mazur's Theorem the torsion group must be a direct product of Z/2Z
        #with the cyclic group generated by the highest order point.
        else:
            print('Z/2Z x ' + 'Z/' + str(highest_order) + 'Z')
        print(C.show_points())

#Elliptic Curves over Prime Order Fields ---------------------------------------------------------

class CurveOverFp(Curve):
    #Construct a Weierstrass cubic y^2 = x^3 + ax^2 + bx + c over Fp.
    def __init__(self, a, b, c, p):
        Curve.__init__(self, a, b, c, p, 1)

    #The secp256k1 curve.
    @classmethod
    def secp256k1(cls):
        return cls(0, 0, 7, 2**256-2**32-2**9-2**8-2**7-2**6-2**4-1)

    def contains(self, P):
        if P.is_infinite():
            return True
        else:
            return (P.y*P.y) % self.char == (P.x*P.x*P.x + self.a*P.x*P.x + self.b*P.x + self.c) % self.char

    def get_points(self):
        #Start with the point at infinity.
        points = [Point.atInfinity()]

        #Just brute force the rest.
        for x in range(self.char):
                for y in range(self.char):
                    P = Point(x,y)
                    if (y*y) % self.char == (x*x*x + self.a*x*x + self.b*x + self.c) % self.char:
                        points.append(P)
        return points

    def invert(self, P):
        if P.is_infinite():
            return P
        else:
            return Point(P.x, -P.y % self.char)

    def add(self, P_1, P_2):
        #Adding points over Fp and can be done in exactly the same way as adding over Q,
        #but with of the all arithmetic now happening in Fp.
        y_diff = (P_2.y - P_1.y) % self.char
        x_diff = (P_2.x - P_1.x) % self.char
        if P_1.is_infinite():
            return P_2
        elif P_2.is_infinite():
            return P_1
        elif x_diff == 0 and y_diff != 0:
            return Point.atInfinity()
        elif x_diff == 0 and y_diff == 0:
            if P_1.y == 0:
                return Point.atInfinity()
            else:
                ld = ((3*P_1.x*P_1.x + 2*self.a*P_1.x + self.b) * mult_inv(2*P_1.y, self.char)) % self.char
        else:
            ld = (y_diff * mult_inv(x_diff, self.char)) % self.char
        nu = (P_1.y - ld*P_1.x) % self.char
        x = (ld*ld - self.a - P_1.x - P_2.x) % self.char
        y = (-ld*x - nu) % self.char
        return Point(x,y)

#Elliptic Curves over Prime Power Order Fields ---------------------------------------------------

class CurveOverFq(Curve):
    #Construct a Weierstrass cubic y^2 = x^3 + ax^2 + bx + c over Fp^n.
    def __init__(self, a, b, c, p, n, irred_poly):
        self.irred_poly = irred_poly
        Curve.__init__(self, a, b, c, p, n)

    #TODO: Implement it!

#Number Theoretic Functions ----------------------------------------------------------------------

def divisors(n):
    divs = [0]
    for i in range(1, abs(n) + 1):
        if n % i == 0:
            divs.append(i)
            divs.append(-i)
    return divs

#Extended Euclidean algorithm.
def euclid(sml, big):
    #When the smaller value is zero, it's done, gcd = b = 0*sml + 1*big.
    if sml == 0:
        return (big, 0, 1)
    else:
        #Repeat with sml and the remainder, big%sml.
        g, y, x = euclid(big % sml, sml)
        #Backtrack through the calculation, rewriting the gcd as we go. From the values just
        #returned above, we have gcd = y*(big%sml) + x*sml, and rewriting big%sml we obtain
        #gcd = y*(big - (big//sml)*sml) + x*sml = (x - (big//sml)*y)*sml + y*big.
        return (g, x - (big//sml)*y, y)

#Compute the multiplicative inverse mod n of a with 0 < a < n.
def mult_inv(a, n):
    g, x, y = euclid(a, n)
    #If gcd(a,n) is not one, then a has no multiplicative inverse.
    if g != 1:
        raise ValueError('multiplicative inverse does not exist')
    #If gcd(a,n) = 1, and gcd(a,n) = x*a + y*n, x is the multiplicative inverse of a.
    else:
        return x % n

#ECDSA functions ---------------------------------------------------------------------------------

#Use sha256 to hash a message, and return the hash value as an integer.
def hash(message):
    return int(sha256(message.encode('utf-8')).hexdigest(), 16)

#Hash the message and return integer whose binary representation is the the L leftmost bits
#of the hash value, where L is the bit length of n.
def hash_and_truncate(message, n):
    h = hash(message)
    b = bin(h)[2:len(bin(n))]
    return int(b, 2)

#Generate a keypair using the point P of order n on the given curve. The private key is a
#positive integer d smaller than n, and the public key is Q = dP.
def generate_keypair(curve, P, n):
    sysrand = SystemRandom()
    d = sysrand.randrange(1, n)
    Q = curve.mult(P, d)
    print("Priv key: d = " + str(d))
    print("Publ key: Q = " + str(Q))
    return (d, Q)

#Create a digital signature for the string message using a given curve with a distinguished
#point P which generates a prime order subgroup of size n.
def sign(message, curve, P, n, keypair):
    #Extract the private and public keys, and compute z by hashing the message.
    d, Q = keypair
    z = hash_and_truncate(message, n)
    #Choose a randomly selected secret point kP then compute r and s.
    r, s = 0, 0
    while r == 0 or s == 0:
        sysrand = SystemRandom()
        k = sysrand.randrange(1, n)
        R = curve.mult(P, k)
        r = R.x % n
        s = (mult_inv(k, n) * (z + r*d)) % n
    print('ECDSA sig: (Q, r, s) = (' + str(Q) + ', ' + str(r) + ', ' + str(s) + ')')
    return (Q, r, s)

#Verify the string message is authentic, given an ECDSA signature generated using a curve with
#a distinguished point P that generates a prime order subgroup of size n.
def verify(message, curve, P, n, sig):
    Q, r, s = sig
    #Confirm that Q is on the curve.
    if Q.is_infinite() or not curve.contains(Q):
        return False
    #Confirm that Q has order that divides n.
    if not curve.mult(Q,n).is_infinite():
        return False
    #Confirm that r and s are at least in the acceptable range.
    if r > n or s > n:
        return False
    #Compute z in the same manner used in the signing procedure,
    #and verify the message is authentic.
    z = hash_and_truncate(message, n)
    w = mult_inv(s, n) % n
    u_1, u_2 = z * w % n, r * w % n
    C_1, C_2 = curve.mult(P, u_1), curve.mult(Q, u_2)
    C = curve.add(C_1, C_2)
    return r % n == C.x % n

#Key Cracking Functions --------------------------------------------------------------------------

#Find d for which Q = dP by simply trying all possibilities
def crack_brute_force(curve, P, n, Q):
    start_time = time()
    for d in range(n):
        if curve.mult(P,d) == Q:
            end_time = time()
            print("Priv key: d = " + str(d))
            print("Time: " + str(round(end_time - start_time, 3)) + " secs")
            break

#Find d for which Q = dP using the baby-step giant-step algortihm.
def crack_baby_giant(curve, P, n, Q):
    start_time = time()
    m = int(ceil(sqrt(n)))
    #Build a hash table with all bP with 0 < b < m using a dictionary. The dicitonary value
    #stores b so that it can be quickly recovered after a matching giant step hash.
    baby_table = {}
    for b in range(m):
        bP = curve.mult(P,b)
        baby_table[str(bP)] = b
    #Check if Q - gmP is in the hash table for all 0 < g < m. If we get such a matching hash,
    #we have Q - gmP = bP, so extract b from the dictionary, then Q = (b + gm)P.
    for g in range(m):
        R = curve.add(Q, curve.invert(curve.mult(P, g*m)))
        if str(R) in baby_table.keys():
            b = baby_table[str(R)]
            end_time = time()
            print("Priv key: d = " + str((b + g*m) % n))
            print("Time: " + str(round(end_time - start_time, 3)) + " secs")
            break

#Find d for which Q = dP using Pollard's rho algorithm. Assumes subgroup has prime order n.
def crack_rho(curve, P, n, Q, bits):
    start_time = time()
    R_list = []
    #Compute 2^bits randomly selected linear combinations of P and Q, storing them as triples
    #of the form (aP + bQ, a, b) in R_list.
    for i in range(2**bits):
        a, b = randrange(0,n), randrange(0,n)
        R_list.append((curve.add(curve.mult(P,a), curve.mult(Q,b)), a, b))
    #Compute a new random linear combination of P and Q to start the cycle-finding.
    aT, bT = randrange(0,n), randrange(0,n)
    aH, bH = aT, bT
    T = curve.add(curve.mult(P,aT), curve.mult(Q,bT))
    H = curve.add(curve.mult(P,aH), curve.mult(Q,bH))
    while True:
        #Advance the tortoise one step, by adding a point in R_list determined by the last b
        #bits in the binary explansion of the x coordinate of the current position.
        j = int(bin(T.x)[len(bin(T.x)) - bits : len(bin(T.x))], 2)
        T, aT, bT = curve.add(T, R_list[j][0]), (aT + R_list[j][1]) % n, (bT + R_list[j][2]) % n
        #Advance the hare two steps, again by adding points in R_list determined by the last
        #b bits in the binary explansion of the x coordinate of the current position.
        for i in range(2):
            j = int(bin(H.x)[len(bin(H.x)) - bits : len(bin(H.x))], 2)
            H, aH, bH = curve.add(H, R_list[j][0]), (aH + R_list[j][1]) % n, (bH + R_list[j][2]) % n
        #If the tortoise and hare arrive at the same point, a cycle has been found.
        if(T == H):
            break
    #It is possible that the tortoise and hare arrive at exactly the same linear combination.
    if bH == bT:
        end_time = time()
        print("Rho failed with identical linear combinations")
        print(str(end_time - start_time) + " secs")
    else:
        end_time = time()
        print("Priv key: d = " + str((aT - aH) * mult_inv((bH - bT) % n, n) % n))
        print("Time: " + str(round(end_time - start_time, 3)) + " secs")

#Find d from two messages signed with the same nonce k. Assumes subgroup has prime order n.
def crack_from_ECDSA_repeat_k(curve, P, n, m1, sig1, m2, sig2):
    Q1, r1, s1 = sig1
    Q2, r2, s2 = sig2
    #Check that the two messages were signed with the same k. This check may pass even if m1
    #and m2 were signed with distinct k, in which case the value of d computed below will be
    #wrong, but this is a very unlikely scenario.
    if not r1 == r2:
        print("Messages signed with distinct k")
    else:
        z1 = hash_and_truncate(m1, n)
        z2 = hash_and_truncate(m2, n)
        k = (z1 - z2) * mult_inv((s1 - s2) % n, n) % n
        d = mult_inv(r1, n) * ((s1 * k) % n - z1) % n
        print("Priv key: d = " + str(d))
