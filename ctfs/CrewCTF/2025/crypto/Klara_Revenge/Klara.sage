#!/usr/bin/env sage

import sys
from Crypto.Util.number import *
import base64
flag=open("flag.txt","rb").read()[:-1]

def die(*args):
	pr(*args)
	quit()
	
def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()
	
def sc(): 
	return sys.stdin.buffer.readline()

Egl=[]
Vugl=[]
Vngl=[]
SMNgl=[]
skeygl=[]


def keygen(nbit):
	global skeygl,Egl,Vugl,Vngl,SMNgl
	p = getPrime(nbit)
	R = PolynomialRing(GF(p), _k2*2, 'x')
	VARS = [R.gen(_) for _ in range(_k2*2)]
	U, V = VARS[:_k2], VARS[_k2:]
	S = list((randint(0, p) for _ in range(_k2**2)))
	skey = matrix(FiniteField(p), _k2, _k2, S)
	skeygl=skey                
	u, v = vector(U[0:_k2:1]), vector(V[0:_k2:1])
	Us, Vs = skey * u, skey * v
	SMN = vector([0] * _k2)
	Vu  = vector(randint(0, p) for _ in range(_k2))
	Vugl=Vu
	SR = []	
	for i in range(_k):
		E = vector(randint(0, p) for _ in range(_k2))
		Egl.append(E)
		if i == _k - 1:
			SMNgl=SMN
			SR.append((E * v) * ((Vu * u) * (Us[2*i]*Vs[2*i+1]+Vs[2*i]*Us[2*i+1])-(SMN*u)*Us[2*i+1]*Vs[2*i+1]))
		else:
			Vn = vector(randint(0, p) for _ in range(_k2))
			Vngl.append(Vn)
			SMN = SMN + Vn
			SR.append((E * v) * ((Vu * u) * (Us[2*i]*Vs[2*i+1]+Vs[2*i]*Us[2*i+1])+(Vn*u)*Us[2*i+1]*Vs[2*i+1]))
		SR.append((E * v) * (Vu * u) * Us[2*i+1]*Vs[2*i+1])
	A = skey.inverse() * vector(SR)
  # We don't really need this...
	#  M = []
	#  for k in range(_k):
		#  SMN = vector([0] * _k2)
		#  Vu  = vector(randint(0, p) for i in range(_k2))
		#  MR = []
		#  for i in range(_k):	
			#  Vr = vector(randint(0, p) for _ in range(_k2))
			#  if (i == _k - 1):
				#  MR.append((Vr * v) * ((Vu * u) * (Us[2*i]*Vs[(2*i+2*k) % _k2])-(SMN*u)*Us[2*i+1]*Vs[(2*i+1+2*k) % _k2]))
				#  MR.append((Vr * v) * (Vu * u) * Us[2*i+1]*Vs[(2*i+1+2*k) % _k2])
			#  else:
				#  E = vector(randint(0, p) for _ in range(_k2))
				#  SMN = SMN + E
				#  MR.append((Vr * v) * ((Vu * u) * (Us[2*i]*Vs[(2*i+2*k) % _k2]) + (E * u) * Us[2*i+1]*Vs[(2*i+1+2*k) % _k2]))
				#  MR.append((Vr * v) * (Vu * u) * Us[2*i+1]*Vs[(2*i+1+2*k) % _k2])
		#  M.append(skey.inverse() * vector(MR))
	return skey, p, A

def SUM(c1, c2):
	e1, e2 = [[randint(0, p)] * _k2 for _ in '__']
	for _ in range(_k2):
		e1[_], e2[_] = c1[_], c2[_]
	S = [0] * _k2
	for i in range(_k2):
		_res = A[i].subs({f"x{k}": e1[k] for k in range(_k2)} | {f"x{k+_k2}": e2[k] for k in range(_k2)}, function = True)
		S[i] = _res(*e1 + e2)
	return vector(S)

def FASTSUM(c1,c2):
  u=c1
  v=c2
  Us=skeygl*u
  Vs=skeygl*v
  SR=[]
  for i in range(_k):
    if i == _k - 1:
      SR.append((Egl[i] * v) * ((Vugl * u) * (Us[2*i]*Vs[2*i+1]+Vs[2*i]*Us[2*i+1])-(SMNgl*u)*Us[2*i+1]*Vs[2*i+1]))
    else:
      SR.append((Egl[i] * v) * ((Vugl * u) * (Us[2*i]*Vs[2*i+1]+Vs[2*i]*Us[2*i+1])+(Vngl[i]*u)*Us[2*i+1]*Vs[2*i+1]))
    SR.append((Egl[i] * v) * (Vugl * u) * Us[2*i+1]*Vs[2*i+1])
  ans = skeygl.inverse() * vector(SR)
  return ans

def MUL(c1, c2):
	e1, e2 = [[randint(0, p)] * _k2 for _ in '__']
	for _ in range(_k2):
		e1[_], e2[_] = c1[_], c2[_]
	c = [0] * _k
	for K in range(_k):
		c[K] = [0] * _k2
		for i in range(_k2):
			_res = M[K][i].subs({f"x{k}": e1[k] for k in range(_k2)} | {f"x{k+_k2}": e2[k] for k in range(_k2)}, function = True)
			c[K][i] = _res(*e1 + e2)
	P = c[0]
	for i in range(1, _k):
		P = FASTSUM(P, c[i])
	return P

def FASTMUL(c1,c2):
  u=c1
  v=c2
  Us=skeygl*u
  Vs=skeygl*v
  M = []
  for k in range(_k):
    SMN = vector([0] * _k2)
    Vu  = vector(randint(0, p) for i in range(_k2))
    MR = []
    for i in range(_k):	
      Vr = vector(randint(0, p) for _ in range(_k2))
      if (i == _k - 1):
        MR.append((Vr * v) * ((Vu * u) * (Us[2*i]*Vs[(2*i+2*k) % _k2])-(SMN*u)*Us[2*i+1]*Vs[(2*i+1+2*k) % _k2]))
        MR.append((Vr * v) * (Vu * u) * Us[2*i+1]*Vs[(2*i+1+2*k) % _k2])
      else:
        E = vector(randint(0, p) for _ in range(_k2))
        SMN = SMN + E
        MR.append((Vr * v) * ((Vu * u) * (Us[2*i]*Vs[(2*i+2*k) % _k2]) + (E * u) * Us[2*i+1]*Vs[(2*i+1+2*k) % _k2]))
        MR.append((Vr * v) * (Vu * u) * Us[2*i+1]*Vs[(2*i+1+2*k) % _k2])
    M.append(skeygl.inverse() * vector(MR))
    e1, e2 = [[randint(0, p)] * _k2 for _ in '__']
  for _ in range(_k2):
    e1[_], e2[_] = c1[_], c2[_]
  c = [0] * _k
  for K in range(_k):
    c[K] = [0] * _k2
    for i in range(_k2):
      c[K][i] = M[K][i]
  P = vector(GF(p),c[0])
  for i in range(1, _k):
    P = FASTSUM(P, vector(GF(p),c[i]))
  return P

def encrypt(m, skey):
	U, V = [vector(randint(1, p - 1) for _ in range(_k)) for _ in '__']
	S = 0
	for i in range(_k - 1):
		S += U[i]
	U[_k - 1] = p - S % p + m
	T = []
	for i in range(_k):
		T += [V[i] * U[i], V[i]]
	return skey.inverse() * vector(T)

def main():
	border = "┃"
	pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr(border, "Welcome to the Klara challenge!! Your mission is to find the flag ", border)
	pr(border, "with given information, have fun and good luck :)                 ", border)
	pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
	nbit = 256
	global p, _k2, _k, A, flag
	_k = 10
	_k2 = 2 * _k
	sleep(1)
	pr(border, f'Generating key, please wait... ')
	skey, p, A = keygen(nbit)
	flag = flag.lstrip(b'crew{').rstrip(b'}')
	l = len(flag)
	m1, m2 = bytes_to_long(flag[:l//2]), bytes_to_long(flag[l//2:])
	e1, e2 = encrypt(m1, skey), encrypt(m2, skey)
	USED=0
	while True:
		pr(	f"{border} Options: \n"
			f"{border}\t[A]dd points \n"
			f"{border}\t[G]et the encrypted flag \n"
			f"{border}\t[M]ultiply points \n"
			f"{border}\t[P]ublic key \n"
			f"{border}\t[Q]uit")
		ans = sc().decode().strip().lower()
		if ans == 'a':
			_b = False
			pr(border, f"Please provide your first point `C1`:")
			_C1 = sc().decode()
			pr(border, f"Please provide your second point `C2`:")
			_C2 = sc().decode()
			try:
				_C1 = [int(_) for _ in _C1.split(',')]
				_C2 = [int(_) for _ in _C2.split(',')]
				if len(_C1) == len(_C2) == _k2 and all(_ < p for _ in _C1) and all(_ < p for _ in _C2):
					_C1, _C2 = vector(GF(p),_C1), vector(GF(p),_C2) 
					_b = True
			except:
				die(border, f"The input you provided is not valid!")
			if _b:
				#  _ADD = SUM(_C1, _C2)
				#  pr(border, f'C1 + C2 = {_ADD}')
				_ADD = FASTSUM(_C1, _C2)
				pr(border, f'C1 + C2 = {_ADD}')
			else:
				die(border, 'Your points are invalid!')
		elif ans == 'g':
			pr(border, f'(e1, e2) = {(e1, e2)}')
		elif ans == 'm':
			if USED>=1:
				continue
			_b = False
			pr(border, f"Please provide your first point `C1`:")
			_C1 = sc().decode()
			pr(border, f"Please provide your second point `C2`:")
			_C2 = sc().decode()
			try:
				_C1 = [int(_) for _ in _C1.split(',')]
				_C2 = [int(_) for _ in _C2.split(',')]
				if len(_C1) == len(_C2) == _k2 and all(_ < p for _ in _C1) and all(_ < p for _ in _C2):
					_C1, _C2 = vector(_C1), vector(_C2) 
					_b = True
			except:
				die(border, f"The input you provided is not valid!")
			if _b:
				_MUL = FASTMUL(_C1, _C2)
				pr(border, f'C1 x C2 = {_MUL}')
				USED+=1
			else:
				die(border, 'Your points are invalid!')
		elif ans == 'p':
		    #Since you can always add anyways, here is A
			pr(border, f'p = {p}')
			pr(border, f'A = {base64.b64encode(dumps(A)).decode()}')
		elif ans == 'q':
			die(border, "Quitting...")
		else:
			die(border, "Bye...")

if __name__ == '__main__':
	main()
