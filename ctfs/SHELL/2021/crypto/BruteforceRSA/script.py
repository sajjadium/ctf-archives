from Crypto.Util.number import bytes_to_long,inverse,getPrime,long_to_bytes
from secret import message
import json

p = getPrime(128)
q = getPrime(128)

n = p * q
e = 65537 

enc = pow(bytes_to_long(message.encode()),e,n)
print("Encrypted Flag is {}".format(enc))

open('./values.json','w').write(json.dumps({"e":e,"n":n,"enc_msg":enc}))
