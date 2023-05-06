import hashlib
import hmac
import os

flag = open("flag.txt", "rb").read()
p = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
a = 0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
b = 0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
E = EllipticCurve(Zmod(p), [a, b])
G = E(0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296,
      0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5)


# RFC 6979 section 2.3.2
def bits2int(b, q):
  res = int.from_bytes(b, 'big')
  blen = res.bit_length() 
  qlen = q.bit_length()
  return res >> (blen - qlen) if qlen < blen else res


# RFC 6979 section 2.3.3
def int2octets(x, q):
  rlen = ceil(q.bit_length()/8)
  return int(x % q).to_bytes(rlen, 'big')


# RFC 6979 section 3.2
def generate_k(hash_func, h, q, x, kp = b""):
  qlen = q.bit_length()//8
  hlen = hash_func().digest_size

  v = b"\x01" * hlen
  k = b"\x00" * hlen
  dgst = hmac.new(k, digestmod=hash_func)
  to_hash = v + b"\x00" + int2octets(x, q) + int2octets(h, q)
  to_hash += kp # Additional data described per variant at section 3.6 (k')
  dgst.update(to_hash)
  k = dgst.digest()

  v = hmac.new(k, v, hash_func).digest()
  dgst = hmac.new(k, digestmod=hash_func)
  to_hash = v + b"\x01" + int2octets(x, q) + int2octets(h, q)
  to_hash += kp # Additional data described per variant at section 3.6 (k')
  dgst.update(to_hash)
  k = dgst.digest()

  v = hmac.new(k, v, hash_func).digest()
  while True:
    t = b""
    while len(t) < qlen:
      v = hmac.new(k, v, hash_func).digest()
      t += v
    k = bits2int(t, q)

    if 1 <= k < q:
      return k

    k = hmac.new(k, v + b"\x00", hash_func).digest()
    v = hmac.new(k, v, hash_func).digest()


def sign(h, q, x, kp = b""):
  print("Signing %x..." % h)
  k = generate_k(hashlib.sha256, h, q, x, kp)
  x1, y1 = (k*G).xy()
  r = Integer(x1)
  s = Integer((h + r*x)*inverse_mod(k, q) % q)
  return r, s


def verify(h, q, r, s, P):
  print("Verifying %x..." % h)
  u1 = h * inverse_mod(s, q) % q
  u2 = r * inverse_mod(s, q) % q
  x1, x2 = (u1*G + u2*P).xy()
  return x1 == r


def get_signature(q, x, kp = b""):
  try:
    h = int(input("hash (hex): "), 16)
  except:
    return False

  if h == int(hashlib.sha256(flag).hexdigest(), 16):
    print("Nonono!")
    return False

  return sign(h, q, x, kp)


def verify_signature(q, P):
  try:
    h = int(input("hash (hex): "), 16)
    r = int(input("r: "))
    s = int(input("s: "))
  except:
    return False
  return verify(h, q, r, s, P)


def verify_password(q, x, kp):
  try:
    password = int(input("password: "))
  except:
    return False
  h = int(hashlib.sha256(flag).hexdigest(), 16)
  return password*E.lift_x(sign(h, q, x, kp)[0]) == G


def menu():
  print()
  print("1- Get signature")
  print("2- Verify signature")
  print("3- Read flag")
  print("4- Exit")
  try:
    option = int(input())
  except:
    return -1
  return option
end


def main():
  q1 = 2 * 2 * 2 * 2 * 3 * 71 * 131 * 373 * 3407
  q2 = 17449 * 38189 * 187019741 * 622491383 * 1002328039319 * 2624747550333869278416773953
  q = int(next_prime(q1*q2))
  x = int(pow(7, q2 * randint(1, p), q))
  P = x*G
  kp = os.urandom(32) # Extra data

  print("\nWelcome! What's your plan for today?")
  while True:
    option = menu()
    if option == 1:
      signature = get_signature(q, x, kp)
      print(signature)
    elif option == 2:
      print("Correct!") if verify_signature(q, P) else print("Wrong!")
    elif option == 3:
      print(flag.decode()) if verify_password(q, x, kp) else print("Wrong!")
    elif option == 4:
      print("Bye!")
      return
    else:
      print("Invalid option!")
      return


main()
