from Crypto.Util import number
import random
import json
import math

rand = random.SystemRandom()
e = 65536
p = number.getStrongPrime(2048)
print(math.gcd(e,p-1))
s = rand.randint(2,p-2)
ssq = pow(s,e,p)
public_key = {
    "p": p,
    "s^e": ssq,
    "e": e
}

private_key = {
    "s": s
}

with open("private_key.json",'w') as f:
    f.write(json.dumps(private_key))

with open("public_key.json","w") as f:
    f.write(json.dumps(public_key))