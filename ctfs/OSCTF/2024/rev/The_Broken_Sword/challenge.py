from Crypto.Util.number import *
from secret import flag,a,v2,pi

z1 = a+flag
y = long_to_bytes(z1)
print("The message is",y)
s = ''
s += chr(ord('a')+23)
v = ord(s)
f = 5483762481^v
g = f*35


r = 14
l = g
surface_area= pi*r*l
w = surface_area//1
s = int(f)
v = s^34
for i in range(1,10,1):
    h = v2*30
    h ^= 34
    h *= pi
    h /= 4567234567342
a += g+v2+f
a *= 67 
al=a
print("a1:",al)
print('h:',h)
