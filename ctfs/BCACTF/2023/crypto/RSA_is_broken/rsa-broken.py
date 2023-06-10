from Crypto.Util.number import *
import math
p = 892582974910679288224965877067
q = 809674535888980601722190167357
n = p * q
e = 65537
message = open('flag.txt', 'rb')
m = bytes_to_long(message.read())
c = pow(m, e, n)
print(f'c = {c}')

# OUTPUT:
# c = 36750775360709769054416477187492778112181529855266342655304

d = pow(e, -1, math.lcm(p-1, q-1))
newm = pow(c, d, n)
print(long_to_bytes(newm))

# OUTPUT:
# b'D\\\x8b\xe3?\x9c\xcd\xa8\xbb(\x80\xa8\xb2\xd8\xffj\x1b\xfbA\x91}\x9e\x89\x00&'
# ??? what
