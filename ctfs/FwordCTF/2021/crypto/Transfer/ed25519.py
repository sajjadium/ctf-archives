from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
import hashlib

b = 256
q = 2**255 - 19
l = 2**252 + 27742317777372353535851937790883648493

d = -121665 * inverse(121666, q) % q
I = pow(2, (q-1)//4, q)

def H(m):
  return hashlib.sha512(m).digest()

def Hint(m):
  return bytes_to_long(H(m))

def add(P, Q):
  x1 = P[0]
  y1 = P[1]
  x2 = Q[0]
  y2 = Q[1]
  x3 = (x1*y2+x2*y1) * inverse(1+d*x1*x2*y1*y2, q) % q
  y3 = (y1*y2+x1*x2) * inverse(1-d*x1*x2*y1*y2, q) % q
  return [x3, y3]

def mult(P, e):
  if e == 0: 
    return [0,1]
  Q = mult(P, e//2)
  Q = add(Q, Q)
  if e & 1: 
    Q = add(Q, P)
  return Q

def isoncurve(P):
  x = P[0]
  y = P[1]
  return (-x**2 + y**2 - 1 - d*x**2*y**2) % q == 0

def recover_x(y):
  xs = (y**2 - 1) * inverse(d*y**2 + 1, q) % q
  x = pow(xs, (q+3)//8, q)
  if (x**2 - xs) % q != 0: 
    x = (x*I) % q
  if x % 2 != 0: 
    x = q-x
  return x

By = 4 * inverse(5, q) % q
Bx = recover_x(By)
B = [Bx % q, By % q]

def bit(h, i):
  return (h[i//8] >> (i%8)) & 1

def point_to_bytes(P):
  x = P[0]
  y = P[1]
  bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
  return ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(b//8)]).encode('latin-1')

def bytes_to_point(s):
  y = sum(2**i * bit(s, i) for i in range(0, b-1))
  x = recover_x(y)
  if x & 1 != bit(s, b-1): 
    x = q-x
  P = [x,y]
  if not isoncurve(P): raise Exception("Decoding point that is not on curve")
  return P
