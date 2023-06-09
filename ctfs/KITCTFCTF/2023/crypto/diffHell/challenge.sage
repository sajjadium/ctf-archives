import hashlib
FLAG = b"GPNCTF{fake_flag}"
def genCommMat(M): 
    u = M[0][0]
    v = M[0][1]
    x = M[1][0]
    y = M[1][1]
    a = M.base_ring().random_element()
    b = M.base_ring().random_element()
    R = M.base_ring()
    c = b*x * v^-1
    d = (a*v + b*y - b*u)*v^-1
    return Matrix(R,[[a,b],[c,d]])

def genGLM(K):
    a,b,c,d = [K.random_element() for _ in [0,0,0,0]]
    M = Matrix(K,[[a,b],[c,d]])
    return M if M.rank() == 2 else genGLM(K)


#starting flag transmission
p = random_prime(2**41,2**42)
A = GL(2,GF(p)).random_element().matrix()
B = genCommMat(A)
G = GL(2,GF(p)).random_element().matrix()
print("Welcome to Dr. Meta's Office. Leading villan since 1980")
print(p)
print("Due to some construction issues there is some information leaking")
print("But rest be assured, to secure his evil plans Dr. Meta has refurbished Cryptography to secure his secrets")
print("Sadly Dr. Meta has lost his keys after gluing himself to an exmatriculation form and his keys to the table below... With his exmatriculation in his hand and his keys on the table can you help out Dr. Meta and decrypt his important data?")


print(G)
print("Look something has fallen from the back of the Turing machine")
print(A^-1*G*A)
gA   = A^-1 * G * A
gB = B ^-1 * G * B 
print("Look we found this on a stack of 'rubbish'")
print(gB)


super_secret_key = B^-1*gA*B
if super_secret_key != A^-1*gB * A :
    print("OHH nooo a MIMA X blew up. The plans to take over the world are destoryed.")

m = hashlib.sha256()
m.update(f"{super_secret_key[0][1]}{super_secret_key[1][0]}{super_secret_key[1][1]}{super_secret_key[0][0]}".encode())
otp = m.digest()
print("Here gulasch spice mix formula to take over the GPN ")
encMsg = [fl^^ot for fl,ot in zip(FLAG,otp)]
print(encMsg)
