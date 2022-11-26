from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b
import random

Zx.<x> = ZZ[]
def convolution(f,g):
  return (f * g) % (x^n-1)

def balancedmod(f,q):
  g = list(((f[i] + q//2) % q) - q//2 for i in range(n))
  return Zx(g)  % (x^n-1)

def randomdpoly(d1, d2):
  result = d1*[1]+d2*[-1]+(n-d1-d2)*[0]
  random.shuffle(result)
  return Zx(result)

def invertmodprime(f,p):
  T = Zx.change_ring(Integers(p)).quotient(x^n-1)
  return Zx(lift(1 / T(f)))

def invertmodpowerof2(f,q):
  assert q.is_power_of(2)
  g = invertmodprime(f,2)
  while True:
    r = balancedmod(convolution(g,f),q)
    if r == 1: return g
    g = balancedmod(convolution(g,2 - r),q)

def keypair():
  while True:
    try:
      f = randomdpoly(61, 60)
      f3 = invertmodprime(f,3)
      fq = invertmodpowerof2(f,q)
      break
    except Exception as e:
      pass
  g = randomdpoly(20, 20)
  publickey = balancedmod(3 * convolution(fq,g),q)
  secretkey = f
  return publickey, secretkey, g

def encode(val):
    poly = 0
    for i in range(n):
        poly += ((val%3)-1) * (x^i)
        val //= 3
    return poly

def encrypt(message, publickey):
  r = randomdpoly(18, 18)
  return balancedmod(convolution(publickey,r) + encode(message), q)


n, q = 263, 128
publickey, _, _ = keypair()

flag = open('flag', 'rb').read()
print(publickey)

for i in range(24):
    print(encrypt(b2l(flag), publickey))
