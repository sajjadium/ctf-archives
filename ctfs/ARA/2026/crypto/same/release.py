from Crypto.Util.number import *
from secrets import *
import ast
import signal

myfavnum = 9

def gen_params():    
    q = getStrongPrime(1024)
    p = 4
    e = getPrime(21)
    while not isPrime(p):                
        k = randbits(1024) + (1 << 1024) 
        p = e * k * q + 1        
    a = (p - 1) // q 
    g = 1
    while g == 1:        
        h = randbelow(p - 3) + 2 
        g = pow(h, a, p)                         
    return (e, p, q, g, randbelow(q-1) + 1) 

def H(msg, e, n):         
    return pow(bytes_to_long(msg)%n, e, n)
    
def sign(params):
    e, m, p, q, g, x, k = params     
    n = p * q
    h = H(m, e, n)               
    r = pow(g, k, p) % q
    s = ((h + x * r) * pow(k, -1, q)) % q        
    return  (r, s, h, q), randbelow(1 << (g%(e>>myfavnum))) + (1 << 1024)


def verify(params):
    e, r, s, m, p, q, g, y = params
    if not (0 < r < q and 0 < s < q):
        return False
    h = H(m, e, p*q)
    try:
        w = pow(s, -1, q)
    except ValueError:
        return False
    u1 = (h * w) % q
    u2 = (r * w) % q    
    v = (pow(g, u1, p) * pow(y, u2, p)) % p
    v = v % q
    return v == r

def msg_sign(params):    
    try:
        msg = bytes.fromhex(input('sign what? (hex) : '))
    except ValueError:
        return False
    e, p, q, g, x, k = params        
    res, k = sign((e, msg, p, q, g, x, k))     
    print(res)
    return k

def check_access(params):
    e, p, q, g, y = params
    n = p * q     
    access_code = token_hex()    
    print(f"code integrity: {H(access_code.encode(),e,n)}") 
    try:
        m_hex, r, s = ast.literal_eval(input("access code and signature? ((m_hex, r, s)) : "))                
        blen = 1 // (int(m_hex, 16) >> 511)
        m = bytes.fromhex(m_hex) 
        r = int(r)
        s = int(s)        
    except:
        return False
    
    if verify((e, r, s, m, p, q, g, y)):          
        return H(m,e,n) == H(access_code.encode(), e, n)      

    return False

def main():    
    e, p, q, g, k = gen_params()    
    privkey = randbits(800) 
    y = pow(g, privkey, p)
    print(f"pub: {y}")
    remaining = list('ARA7!')
    while remaining:
        usr_input = input("sign or get access? (s/g/e for exit) : ").strip().lower()

        if usr_input == "s":
            new_k = msg_sign((e, p, q, g, privkey, k))

            if new_k:
                k = new_k
                remaining.pop()
            else:                                
                k = randbelow(1 << (g%(e>>myfavnum))) + (1 << 1024)
                print("Invalid message!")

        elif usr_input == "g":
            if check_access((e, p, q, g, y)):
                print("ACCESS GRANTED!")
            else:
                print("ACCESS DENIED! CHEAT DETECTED!")
            break

        elif usr_input == "e":
            print("Bye.")
            break

        else:
            print("Invalid input.")

    else:
        print("Thanks!")

if __name__ == "__main__":    
    signal.alarm(myfavnum)
    main()
