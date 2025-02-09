from Crypto.Util.number import getPrime, bytes_to_long

def GenerateKeys(p, q):
    e = 65537
    n = p * q
    phi = (p-1)*(q-1)
    d = pow(e, -1, phi)
    C = 0xbaaaaaad
    D = 0xdeadbeef
    A= 0xbaadf00d
    K = (A*p**2 - C*p + D)*d
    return (e, n, K)

def Encrypt():
    flag = b"REDACTED" # HEHEHEHEHE
    p = getPrime(512)
    q = getPrime(512)
    e, n, K = GenerateKeys(p, q)
    pt = bytes_to_long(flag)
    ct = pow(pt, e, n)
    
    print(f"e = {e}")
    print(f"n = {n}")
    print(f"ct = {ct}")
    print(f"K = {K}")

Encrypt()
