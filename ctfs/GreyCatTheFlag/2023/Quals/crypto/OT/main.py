import secrets
import hashlib
from Crypto.Util.number import isPrime, long_to_bytes

FLAG = b'grey{fake_flag}'

e = 0x10001

def checkN(N):
    if (N < 0):
        return "what?"
    if (N.bit_length() != 4096):
        return "N should be 4096 bits"
    if (isPrime(N) or isPrime(N + 23)):
        return "Hey no cheating"
    return None
    
def xor(a, b):
    return bytes([i ^ j for i,j in zip(a,b)])

def encrypt(key, msg):
    key = hashlib.shake_256(long_to_bytes(key)).digest(len(msg))
    return xor(key, msg)

print("This is my new Oblivious transfer protocol built on top of the crypto primitive (factorisation is hard)\n")
print("You should first generate a number h which you know the factorisation,\n")
print("If you wish to know the first part of the key, send me h")
print(f"If you wish to know the second part of the key, send me h - {23}\n")

N = int(input(("Now what's your number: ")))

check = checkN(N)
if check != None:
    print(check)
    exit(0)

k1, k2 = secrets.randbelow(N), secrets.randbelow(N)
k = k1 ^ k2

print("Now I send you these 2 numbers\n")
print(f"pow(k1, e, N) = {pow(k1, e, N)}")
print(f"pow(k2, e, N+23) = {pow(k2, e, N + 23)}\n")

print("Since you only know how to factorise one of them, you can only get one part of the data :D\n")
print("This protocol is secure so sending this should not have any problem")
print(f"flag = {encrypt(k, FLAG).hex()}")
print("Bye bye!")

