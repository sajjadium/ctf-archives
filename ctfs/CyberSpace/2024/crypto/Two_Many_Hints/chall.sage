from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad

from secret import flag

# PARAMETERS
q       = 3329
k       = 2 
sigma   = 2.5
n       = 256
K = CyclotomicField(n,'z') 
OK      = K.OK()
OKq= OK.quotient(q,'y')

A = matrix(K, k,k, [K(random_vector(ZZ,n//2,x=-q//2,y=q//2).list()) for _ in k*k*"_"]).lift_centered()
s = matrix(K, [K(random_vector(ZZ,n//2,sigma,distribution="gaussian").list()) for __ in k*"_"] )
e = matrix(K, [K(random_vector(ZZ,n//2,sigma,distribution="gaussian").list()) for __ in k*"_"] )
b = (s*A +e ).change_ring(OKq)  



H = matrix(k,k,[ OK(list(random_vector(ZZ,n))) for _ in k*k*"_"] )
l = s*H                                                # I won't give you this 3:)
h = floor(.25*n/2)                                                 
l2 = matrix([l[0,0] , OK(l[0,1].list()[:-h]) ]) 

key = sha256(str(s).encode()).digest()[:16]
iv  = sha256(str(e).encode()).digest()[:16]

cipher= AES.new(key,AES.MODE_CBC,iv=iv)

enc = cipher.encrypt(pad(flag,16))

#Printing 
print(f"A  = {A.coefficients()}")
print(f"b  = {b.coefficients()}")
print(f"H  = {H.coefficients()}")
print(f"l2 = {l2.coefficients()}")
print("enc = ", enc.hex())
