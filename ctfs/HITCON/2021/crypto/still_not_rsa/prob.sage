from Crypto.Util.number import bytes_to_long as b2l
from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Cipher import AES
from hashlib import sha256
import random, os, binascii

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
  g = randomdpoly(15, 15)
  publickey = balancedmod(3 * convolution(fq,g),q)
  secretkey = f
  return publickey, secretkey, g

def encode(val):
    poly = 0
    for i in range(n):
        c = val % q 
        poly += (((c + q//2) % q) - q//2) * (x^i)
        val //= q
    return poly

def decrypt(ciphertext, secretkey):
  f = secretkey
  f3 = invertmodprime(f,3)
  a = balancedmod(convolution(encode(ciphertext), f), q)
  return balancedmod(convolution(a, f3), 3)

n, q = 167, 128
publickey, secretkey, _ = keypair()

flag = open('flag', 'rb').read()
flag += (16 - len(flag)%16) * b'\x00'
key = sha256(str(secretkey).encode()).digest()
iv = os.urandom(16)
flag_enc = AES.new(key, AES.MODE_CBC, iv).encrypt(flag)
print(iv.hex())
print(flag_enc.hex())
print(publickey)
try:
    for _ in range(1000):
        msg = binascii.unhexlify(input())
        print(decrypt(b2l(msg), secretkey))
except Exception as e:
    pass
