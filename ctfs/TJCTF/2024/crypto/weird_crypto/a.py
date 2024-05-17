from math import lcm
from Crypto.Util.number import bytes_to_long, getPrime

with open('flag.txt', 'rb') as f:
    flag = bytes_to_long(f.read().strip())

oops = getPrime(20)
p1 = getPrime(512)
p2 = getPrime(512)

haha = (p1-1)*(p2-1)
crazy_number = pow(oops, -1, haha)
discord_mod = p1 * p2
hehe_secret = pow(flag, crazy_number, discord_mod)

print('admin =', discord_mod)
print('hehe_secret =', hehe_secret)
print('crazy number =', crazy_number)
