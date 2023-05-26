from Crypto.Util.number import bytes_to_long

p = random_prime(2 ^ 650)
q = random_prime(2 ^ 650)
N = p*q
e = 5
flag = open("flag.txt", "rb").read().strip()
m = bytes_to_long(b'the challenges flag is ' + flag)
c = m ^ e % N
print("N: ", N)
print("C: ", c)
print("e: ", e)
