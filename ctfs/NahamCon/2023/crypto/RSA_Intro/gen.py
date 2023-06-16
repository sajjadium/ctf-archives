from Crypto.Util.number import getStrongPrime, getPrime, bytes_to_long as b2l

FLAG = open('flag.txt', 'r').read().strip()
OUT = open('output.txt', 'w')

l = len(FLAG)
flag1, flag2, flag3 = FLAG[:l//3], FLAG[l//3:2*l//3], FLAG[2*l//3:]

# PART 1
e = 0x10001
p = getStrongPrime(1024)
q = getStrongPrime(1024)
n = p*q
ct = pow(b2l(flag1.encode()), e, n)
OUT.write(f'*** PART 1 ***\ne: {e}\np: {p}\nq: {q}\nct: {ct}')

# PART 2
e = 3
p = getStrongPrime(1024)
q = getStrongPrime(1024)
n = p*q
ct = pow(b2l(flag2.encode()), e, n)
OUT.write(f'\n\n*** PART 2 ***\ne: {e}\nn: {n}\nct: {ct}')

# PART 3
e = 65537
p = getPrime(24)
q = getPrime(24)
n = p*q

fl = round(len(flag3)/4)
f3_parts = [flag3[i:i+4] for i in range(0, len(flag3), 4)]
assert ''.join(f3_parts) == flag3
ct_parts = []
for part in f3_parts:
    pt = b2l(part.encode())
    assert pt < n
    ct = pow(pt, e, n)
    ct_parts.append(ct)

OUT.write(f'\n\n*** PART 3 ***\ne: {e}\nn: {n}\nct: {ct_parts}')
