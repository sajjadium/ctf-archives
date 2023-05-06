from Crypto.Util.number import getPrime,isPrime,bytes_to_long
from Crypto.PublicKey.RSA import construct
from secret import flag


def getNextPrime(number):
    while not isPrime(number):
        number+=1
    return number

p = getPrime(2048)
q = getNextPrime(p+1)
n = p*q
e = 65537
encrypted_flag = pow(bytes_to_long(flag.encode('utf-16')),e,n)
print("Public Key = \n{}".format(construct((n,e)).publickey().exportKey().decode()))
print("Encrypted Flag = {}".format(hex(encrypted_flag)))
