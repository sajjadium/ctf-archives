from Crypto.Util.number import *


with open('flag.txt','rb') as f:
    flag = f.read().strip()

e=65537
p=getPrime(256)
q=getPrime(256)
n=p*q
phi=(p-1)*(q-1)
m=bytes_to_long(flag)
d=pow(e,-1,phi)
ct=pow(m,e,n)

print ('n:',n)
print ('e:',e)
print ('ct:',ct)

def enc(msg):
    print (d%msg)
try:
    br="#"
    print (br*70)
    print ("Now here's the More part!!!")
    print ("Enter some number, and I will encrypt it for you")
    print ("But you gotta follow the condition that your number gotta be less than 2^140 (and like legitamite)")
    print (br*70)
    s=int(input("Enter: ").strip())
    assert(s>0 and s<2**140)
    enc(s)
except:
    print ("Bruh why you be like this")
    exit()
