M, s, l, C = 7777771, [], 1337, [] 
n=[]
flag = "REDACTED"

k = [list(map(int, list(' '.join(bin(ord(i))[2:]).split()))) for i in flag]

def num_gen(first, last):

   o = [[1]]                       
   cnt = 1                            
   while cnt <= last:
       if cnt >= first:
           yield o[-1][0]           
       row = [o[-1][-1]]            
       for b in o[-1]:
        row.append(row[-1] + b)  
       cnt += 1                       
       o.append(row)
           
for i in num_gen(7, 13):
       s.append(i)
              
for i in range(len(s)):
    ni = ((l*s[i]) % M)           
    n.append(ni)


for p in k:
    C_curr = []
    for (x,y) in zip(p, n):
        C_ = x*y
        C_curr.append(C_)
    C += [sum(C_curr)]

print(M, s, l, C, n)


