#Elliptic curve basics, tools for finding rational points, and ECDSA implementation.
#Brendan Cordy, 2015

from fractions import Fraction
from math import ceil, sqrt
from random import SystemRandom, randrange
from hashlib import sha256
from time import time
import pyotp
import datetime

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
        f = open("otp_seed.txt", "r")
        seed = f.readline().strip()
        f.close()
        self.hotp = pyotp.HOTP(seed)


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

    #Generate a secure OTP based on minutes and seconds with a 10 second slack
    def getRandomOTP(self):
        now = datetime.datetime.now()
        return int(self.hotp.at( (now.minute + 1) * (now.second // 10) ))

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
            # print('\t', (P.y*P.y) % self.char)
            # print('\t', (P.x*P.x*P.x + self.a*P.x*P.x + self.b*P.x + self.c) % self.char )
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

#Use sha256 to hash a message, and return the hash value as an interger.
def hash(message):
    # return int(sha256(message).hexdigest(), 16)
    return int(sha256(str(message).encode('utf-8')).hexdigest(), 16)

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
    return (d, Q)

#Create a digital signature for the string message using a given curve with a distinguished
#point P which generates a prime order subgroup of size n.
def sign(message, curve, P, n, keypair):
    #Extract the private and public keys, and compute z by hashing the message.
    d, Q = keypair # 130,(1341,1979)
    z = hash_and_truncate(message, n) # 0xfb
    #Choose a randomly selected secret point kP then compute r and s.
    r, s = 0, 0
    while r == 0 or s == 0:
        k = curve.getRandomOTP()
        R = curve.mult(P, k)
        r = R.x % n
        s = (mult_inv(k, n) * (z + r*d)) % n
    print('ECDSA sig of \"' + message+ '\" : (Q, r, s) = (' + str(Q) + ', ' + str(r) + ', ' + str(s) + ')')
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