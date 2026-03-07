from Crypto.Util.number import *
import secrets

while True:
  p=6*getPrime(512)-1
  if is_prime(p):
    break


E=EllipticCurve(GF(p),[0,1])
G1=E.gens()[0]
G1*=6
o=G1.order()

Fp2=GF(p**2,'x',modulus=[1,1,1])
E2=EllipticCurve(Fp2,[0,1])
G1=E2(G1)

while True:
  G2=E2.random_point()
  G2*=6
  if G2.weil_pairing(G1,o)!=1:
    break

MxDeg=40
Q=100

def setup(deg=40):
  alpha=secrets.randbelow(o)
  vec=[]
  Pt=G1
  Pol=[0 for i in range(deg)]
  for i in range(deg):
    vec.append(Pt)
    Pol[i]=secrets.randbelow(o)
    Pt*=alpha
  
  PP=sum([pow(alpha,i,o)*Pol[i] for i in range(deg)])
  Pol[0]-=PP
  Pol=[a%o for a in Pol]
  
  Pub=[(a,b) for (a,b) in zip(vec,Pol)]
  for i in range(len(Pub)-1,0,-1):
    # Whoops!
    j=secrets.randbelow(i+1)
    Pub[j],Pub[i]=Pub[i],Pub[j]
  
  assert(sum([a*b for (a,b) in Pub])==0)
  G2alpha=G2*alpha
  return Pub,G2alpha

def readpoint(s):
  # Reads point from E
  Pt=list(map(int,input(s).split(",")))
  assert(len(Pt)==2)
  Pt=E(Pt)
  assert(Pt!=0)
  assert(Pt.order()==o)
  return E2(Pt)

def open_comm(z,pi,r,G2alpha):
  # Open polynomial at point z
  # Proving that p(z)=y, with witness pi
  y=int(input("y = "))
  pi=readpoint("pi = ")
  # pair(pi,G2alpha-z*G2) == pair(C-y*G1,G2)
  
  assert(pi.weil_pairing(G2alpha-z*G2,o)==(C-y*G1).weil_pairing(G2,o))
  return y
  

if __name__=="__main__":
  print(f"{p = }")
  pub,G2alpha=setup(MxDeg)
  pub2=[((a.x(),a.y()),b) for (a,b) in pub]
  print(f"pub = {pub2}")
  
  C=readpoint("C = ") #Commit to a polynomial
  pairs=[]
  for i in range(Q):
    z=secrets.randbelow(p)
    print(f"{z = }")
    y=open_comm(z,pi,r,G2alpha)
    pairs.append((z,y))
  
  
  R=PolynomialRing(GF(o),'x')
  pol=R.lagrange_polynomial(pairs)
  
  if pol.degree()>MxDeg:
    print("WHAT!")
    print(open("flag.txt","r").read())
  else:
    print("Ok!")
  

