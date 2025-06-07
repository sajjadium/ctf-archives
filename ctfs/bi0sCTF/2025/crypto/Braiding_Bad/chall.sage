import random
import string
import hashlib
from Crypto.Util.number import bytes_to_long

message = <REDACTED>

n = 100
Bn = BraidGroup(n)
gs = Bn.gens()
K = 32

gen = gs[n // 2 - 1]
p_list = [gen] + random.choices(gs, k=K-1)
p = prod(p_list)
print(f"p: {list(p.Tietze())}")

a = prod(random.choices(gs[:n//2-2], k=K))
q = a * p * a^-1
print(f"q: {list(q.Tietze())}")

br = prod(random.choices(gs[n//2 + 1:], k=K))
c1 = br * p * br^-1
c2 = br * q * br^-1

h = hashlib.sha512(str(prod(c2.right_normal_form())).encode()).digest()

original_message_len = len(message)
pad_length = len(h) - original_message_len
left_length = random.randint(0, pad_length)
pad1 = ''.join(random.choices(string.ascii_letters, k=left_length)).encode('utf-8')
pad2 = ''.join(random.choices(string.ascii_letters, k=pad_length - left_length)).encode('utf-8')
padded_message = pad1 + message + pad2

d_str = ''.join(chr(m ^^ h) for m, h in zip(padded_message, h))
d = bytes_to_long(d_str.encode('utf-8'))

print(f"c1: {list(c1.Tietze())}")
print(f"c2: {d}")