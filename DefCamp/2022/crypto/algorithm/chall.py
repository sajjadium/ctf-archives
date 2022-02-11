flag = ' [test]'
hflag = flag.encode('hex')
iflag = int(hflag[2:], 16)

def polinom(n, m):
   i = 0
   z = []
   s = 0
   while n > 0:
   	if n % 2 != 0:
   		z.append(2 - (n % 4))
   	else:
   		z.append(0)
   	n = (n - z[i])/2
   	i = i + 1
   z = z[::-1]
   l = len(z)
   for i in range(0, l):
       s += z[i] * m ** (l - 1 - i)
   return s

i = 0
r = ''
while i < len(str(iflag)):
   d = str(iflag)[i:i+2]
   nf = polinom(int(d), 3)
   r += str(nf)
   i += 2

print r 
