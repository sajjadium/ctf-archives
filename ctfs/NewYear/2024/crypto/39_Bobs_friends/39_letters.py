from Crypto.Util.number import getPrime, bytes_to_long

flag = b'grodno{fake_flag}'
m = bytes_to_long(flag)
e = 39
n = [getPrime(1024) * getPrime(1024) for i in range(e)]
c = [pow(m, e, n[i]) for i in range(e)]

open("all_letters.txt", 'w').write(f"e = {e}\nc = {c}\nn = {n}")
