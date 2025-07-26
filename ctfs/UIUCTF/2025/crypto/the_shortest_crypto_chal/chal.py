from Crypto.Cipher import AES
from hashlib import md5
from secret import a,b,c,d, FLAG

assert a**4 + b**4 == c**4 + d**4 + 17 and max(a,b,c,d) < 2e4 and AES.new( f"{a*b*c*d}".zfill(16).encode() , AES.MODE_ECB).encrypt(FLAG).hex() == "41593455378fed8c3bd344827a193bde7ec2044a3f7a3ca6fb77448e9de55155"
