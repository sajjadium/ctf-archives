from Crypto.Util.number import getStrongPrime
from os import getenv

BITS = 512

def gen_key():
    p = getStrongPrime(BITS)
    q = getStrongPrime(BITS)
    n = p*q
    e = 65537

    return (p, q, e)

def safe_encrypt(key, msg):
    p, q, e = key
    n = p*q
    pt = int(msg, 16)
    if pt > p:
        return b'Error: message to encrypt is too big'
    elif pt < 0:
        return b'Error: message is negative'
    ct = pow(pt, e, n)

    return hex(ct)[2:]


key = gen_key()
p, q, e = key
FLAG = getenv('FLAG', 'ptm{fakeflag}').encode()

print('Welcome to my super safe RSA encryption service!')
print('Big primes and small messages ensure 100% secrecy!')

if __name__ == '__main__':
    while True:
        print('1) Encrypt a message')
        print('2) Get encrypted flag')
        choice = int(input('> '))
        if choice == 1:
            msg = input('Enter your message in hex: ')
            ct = safe_encrypt(key, msg)
            print(ct)
        elif choice == 2:
            ct = safe_encrypt(key, FLAG.hex())
            print(ct)
        else:
            print('Goodbye!')
            break

