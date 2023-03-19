from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def encrypt(numToEncrypt):
    def getPrimeCustom(bitLength, e):
        while True:
            i = getPrime(bitLength)
            if (i-1) % e**2 == 0:
                return i

    global e
    global C
    bitLength = ((len(bin(numToEncrypt)) - 2) // 2) + 9
    e = 113
    p = getPrimeCustom(bitLength, e)
    q = getPrimeCustom(bitLength, e)
    N = p * q
    print(f"N = {N}")
    C = pow(numToEncrypt, e, N)
    return C

msg = b"wsc{????????????????????}"
numToEncrypt = bytes_to_long(msg)

# maybe if I keep encrypting it will fix itself???
# surely it won't make it worse
encryptedNum = encrypt(numToEncrypt)
for x in range(26):
    encryptedNum = encrypt(encryptedNum)
  
print(f"e = {e}")
print(f"C = {C}")
