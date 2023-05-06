from Crypto.Util.number import *

with open('flag.txt','rb') as g:
    flag = g.read().strip()

with open('nums.txt','r') as f:
	s=f.read().strip().split()
	a=int(s[0])
	b=int(s[1])
	c=int(s[2])


e=65537
n=a**3+b**3-34*c**3
m=bytes_to_long(flag)
ct=pow(m,e,n)


print ("n: ",n)
print ("e: ",e)
print ("ct: ",ct)

