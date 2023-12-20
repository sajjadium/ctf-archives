from Crypto.Util.number import *

flag = "This flag has been REDACTED"
moduli = "This array has been REDACTED"

m = bytes_to_long(flag.encode())
e = 3
remainders = [pow(m,e,n) for n in moduli]

f = open('output.txt','w')
for i in range(len(moduli)):
    f.write(f"m ^ e mod {moduli[i]} = {remainders[i]}\n")
f.write(f"\ne = {e}")
f.close()