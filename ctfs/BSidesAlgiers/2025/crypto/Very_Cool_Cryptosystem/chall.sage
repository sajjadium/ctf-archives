from flag import flag
assert len(flag) == 110 

p = random_prime(2**100)
q = random_prime(2**100)
n = p * q


Rn = Zmod(n)
SIZE = 4 
M = GL(SIZE, Rn)

def matrix_random():
    while True:
        try :
            rands = [randint(0, n-1) for _ in range(SIZE ** 2)]
            Mat = M(rands)
            return Mat
        except : 
            continue


#Making My Private KEY Not So Important
def priv_key(flag1) :
    m = Rn(int.from_bytes(flag1.encode(),"big"))  
    a = Rn(randint(0, n-1))
    coeffs = SIZE - 1 
    bound = coeffs * (coeffs + 1) // 2
    b_s = [Rn(randint(0, n)) for _ in range(bound)]  
    c = m ** bound
    c_s = []
    for i in range(coeffs):
        t = i * (i + 1) // 2
        o = ((c +  b_s[t]) if t else c ) ** 5 
        if not i:
            c_s.append((a * o + b_s[t]))
            continue
        for j in range(0, i):
            o *= a 
            o += b_s[t + j + 1]
        c_s.append(o)

    diag = [a**i + c for i in range(1,5)]
    Mat = Matrix(Rn, [ i * [0] + [diag[i]] +  ([c_s[i] ] if i < len(c_s) else []) + (2-i) * [ ((b_s[i] + b_s[i+1])*a)**20 ]  for i in range(4)] )
    return M(Mat) , b_s  

def gen_pub(derived):
    r = 5
    while True:
        A = matrix_random()
        D , b_s  = priv_key(derived)
        try:
            if D * A != A * D:
                Dr = D^r
                B = (~D) * (~A) * D
                pubkey = ( A , B , Dr)
                return pubkey , b_s ,D
        except:
            continue


def encrypt(pub , flag2):
    s = randint(1 , 2**10)
    gam = pub[-1] ^ s
    eps = ~gam * pub[0] * gam 
    k = ~gam * pub[1] * gam 
    length = len(flag2) // 16 
    U = M(Matrix(Rn , 4 , 4 , [ int.from_bytes(flag2[i*length : (i+1)*length].encode() , "big") for i in range(16) ]))
    U_ = k * U * k 
    return U_ , eps

pub , b_s , D   = gen_pub(flag[:30])
U_ , eps = encrypt(pub , flag[30:])



# Output  ..........
with open("out.txt" , "w") as f :    
    Dr = Matrix(pub[-1])
    eps = eps.list()
    U_ = U_.list()
    A = pub[0].list()
    f.write(f"{n = }\n")
    f.write(f"{b_s = }\n")
    for i in range(3):
        f.write(f"Dr[{i}][{i+1}] = { Dr[i][i+1] }\n")
    f.write(f"{A = }\n")
    f.write(f"{eps = }\n")
    f.write(f"{U_ = }\n")







