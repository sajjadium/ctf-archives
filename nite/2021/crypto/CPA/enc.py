from sage.all import *
from Crypto.Util.number import bytes_to_long
from FLAG import flag

f = flag

def make_matrix(n):
    zn = IntegerModRing(n)
    mat_list = [randint(0, n-1) for i in range(4)]
    mat = [[mat_list[0], mat_list[1]], [mat_list[2], mat_list[3]]]
    mat = Matrix(zn, mat)
    return mat

def enc(pt,n):
    alpha = make_matrix(n)
    X = make_matrix(n)

    while X*alpha.inverse() == alpha*X or alpha.is_invertible == False or X.is_invertible == False :
        alpha = make_matrix(n)
        X = make_matrix(n)
    
    beta =X.inverse()*alpha.inverse()*X

    r = randint(1, 2**512)
    gamma = X**r

    s = randint(1, 2**512)
    delta = gamma**s
    epsilon = delta.inverse()*alpha*delta
    k = delta.inverse()*beta*delta

    ct = k*pt*k
    return (alpha,beta,gamma,ct,epsilon)

p = random_prime(2**256)
q = random_prime(2**256)
n = p*q

long_flag = bytes_to_long(f)
l = len(str(long_flag))
q = l//4

pt = []
for i in range(4):
    pt.append((str(long_flag)[i*q:(i+1)*q]))
    if pt[i].startswith('0'):
        pt[i-1] += '0'

p = [int(i) for i in pt]

pt = [[p[0],p[1]],[p[2],p[3]]]
pt = Matrix(pt)

pub = enc(pt,n)

#CREATING MATRIX LINEAR EQUATIONS

#A*X + B*Y = C
#D*X + E*Y = F


A = make_matrix(n)
B = make_matrix(n)
D = make_matrix(n)
E = make_matrix(n)
C = A*X + B*Y 
F = D*X + E*Y

while A.is_invertible()==False or B.is_invertible()==False or C.is_invertible()==False or D.is_invertible()==False or E.is_invertible()==False or F.is_invertible()==False:
    A = make_matrix(n)
    B = make_matrix(n)
    D = make_matrix(n)
    E = make_matrix(n)
    C = A*X + B*Y 
    F = D*X + E*Y

print('n:', n)
print('alpha: ', pub[0])
print('beta:', pub[1])
print('gamma:', pub[2])
print('cipher text:', pub[3])

print('-'*440)

print('A:',A)
print('B:',B)
print('C:',C)
print('D:',D)
print('E:',E)
print('F:',F)