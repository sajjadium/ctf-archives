from Crypto.Util.number import long_to_bytes, bytes_to_long, isPrime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Can you undo this?
from hidden import p,N,a,flag,g

# these are for you :)
assert isPrime(p)
assert len(bin(a)) < 1050

hint = pow(g, a, p)
key = long_to_bytes(a)[:16]

cipher = AES.new(key, AES.MODE_ECB)
ct = cipher.encrypt(pad(flag, AES.block_size))

# Now for your hints
print(f"g = {g}")
print(f"P = {p}")
print(f"ciphertext = {ct}")
print(f"Hint = {hint}")
