import os

e = 3

p = random_prime(2^1024-1, lbound=2^1023)
assert p % e != 1
q = random_prime(2^1024-1, lbound=2^1023)
assert q % e != 1
n = p * q

flag_inner = os.environ["FLAG"].encode()
assert len(flag_inner) == 16
flag = b"VuwCTF{" + flag_inner + b"}"

c_flag_inner = pow(int.from_bytes(flag_inner), e, n)
c_flag = pow(int.from_bytes(flag), e, n)

print(f"{e=}")
print(f"{n=}")
print(f"{c_flag_inner=}")
print(f"{c_flag=}")
