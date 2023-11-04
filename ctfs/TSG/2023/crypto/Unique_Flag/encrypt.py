from Crypto.Util.number import getPrime

p = getPrime(1024)
q = getPrime(1024)
N = p * q
e = 0x10001

with open('flag.txt', 'rb') as f:
    flag = f.read()

assert len(flag) == 33

flag_header = flag[:7] # TSGCTF{
flag_content = flag[7:-1]
flag_footer = flag[-1:] # }

assert len(flag_content) == len({byte for byte in flag_content}) # flag_content is unique

c_list = [pow(byte, e, N) for byte in flag]
clues = [x * y % N for x, y in zip(c_list[:-1], c_list[1:])]
clues.sort()

print(f'N = {N}')
print(f'e = {e}')
print(f'clues = {clues}')
