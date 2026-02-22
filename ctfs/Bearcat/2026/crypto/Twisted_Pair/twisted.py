import random
from Crypto.Util.number import getPrime, GCD, bytes_to_long

def genRSA():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p*q
    phi = (p-1)*(q-1)
    e = 65537
    d = pow(e, -1, phi)
    if GCD(e, phi) != 1:
        return genRSA()
    return (n, e), (phi, d)

def main():
    with open('flag.txt','rb') as f:
        flag = f.read()
    m = bytes_to_long(flag)
    pub, priv = genRSA()
    n, e = pub
    phi, d = priv
    c = pow(m,e,n)
    print(f'{e = }')
    print(f'{n = }')
    print(f'{c = }')
    
    big_phi = random.randint(0,n)*phi
    while True:
        re = random.randint(0,big_phi)
        if GCD(re,big_phi) == 1:
            break
    rd = pow(re,-1,big_phi)
    pair = (re,rd)
    print(f'{pair = }')

if __name__ == '__main__':
    main()