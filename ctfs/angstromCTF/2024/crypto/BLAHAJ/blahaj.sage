p = random_prime(2**1024)
q = random_prime(2**1024)
a = randint(0, 2**1024)
b = randint(0, 2**1024)

def read_flag(file='flag.txt'):
    with open(file, 'rb') as fin:
        flag = fin.read()
    return flag

def pad_flag(flag, bits=1024):
    pad = os.urandom(bits//8 - len(flag))
    return int.from_bytes(flag + pad, "big")

def generate_keys(p, q):
    n = p * q
    e = 0x10001
    return n, e

def encrypt_message(m, e, n):
    return pow(m, e, n)

flag = read_flag()
m = pad_flag(flag)

n, e = generate_keys(p, q)
assert m < n

c = encrypt_message(m, e, n)

print(c)
print(n)
print(p + b * q)
print(a * p + q)
