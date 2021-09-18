from random import *

def gen():
  mod=randint(10**9,10**10)
  while (mod%2==0):
    mod=randint(10**9,10**10)
  return mod

mod=gen()
small=mod
while True:
  for i in range(2,int((mod+5)**(1/2))):
    if mod%i==0:
      small=i
      break
  if small!=mod:
    mod*=small
    break
  mod=gen()

lst=[]
for i in range(small-1):
  lst.append(1)
r=randint(min(10,small-1),small*3)
for i in range(r):
  lst.append(0)
  
shuffle(lst)
print ("Alright, I will send you a string, where each char contains either 0 or 1.")
print ("Then you will send me a list of integers back with the same size, separated by spaces.")
print ("Now for each number in your list, a, if it satisfies a to the power of "+str(small)+" is congruent to 1 mod "+str(mod)+" it will encode to 1.")
print ("Otherwise, your number will encode to 0. Now I will concattenate all of your encoded numbers into a string.")
print ("If this string equals the original string I sent you, then you will get the flag :yayy:.")
print ("One final caveat: all your numbers must be unique and positive integers greater than 1 and less than "+str(mod)+".")
string=""
for i in lst:
  string+=str(i)
print (string)

s=input("Enter: ").strip().split()
s=[int(i) for i in s]
check=True
for i in s:
  if i>=mod or i<=1:
    check=False
    break
check=check & (len(s)==len(lst))
check=check & (len(s)==len(set(s)))

cs=""
for i in s:
  if pow(i,small,mod)==1:
    cs+="1"
  else:
    cs+="0"
check=check & (cs==string)

if check:
  with open('flag.txt','rb') as f:
      flag = f.read().strip()
  print (flag)
else:
  print ("Better luck next time!")
