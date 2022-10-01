#!/usr/local/bin/python
#
# Polymero
#

# Imports
from Crypto.Util.number import isPrime, getPrime, inverse
import hashlib, time, os

# Local import
FLAG = os.environ.get('FLAG').encode()


class URSA:
    # Upgraded RSA (faster and with cheap key cycling)
    def __init__(self, pbit, lbit):
        p, q = self.prime_gen(pbit, lbit)
        self.public = {'n': p * q, 'e': 0x10001}
        self.private = {'p': p, 'q': q, 'f': (p - 1)*(q - 1), 'd': inverse(self.public['e'], (p - 1)*(q - 1))}
        
    def prime_gen(self, pbit, lbit):
        # Smooth primes are FAST primes ~ !
        while True:
            qlst = [getPrime(lbit) for _ in range(pbit // lbit)]
            if len(qlst) - len(set(qlst)) <= 1:
                continue
            q = 1
            for ql in qlst:
                q *= ql
            Q = 2 * q + 1
            if isPrime(Q):
                break
        while True:
            plst = [getPrime(lbit) for _ in range(pbit // lbit)]
            if len(plst) - len(set(plst)) <= 1:
                continue
            p = 1
            for pl in plst:
                p *= pl
            P = 2 * p + 1
            if isPrime(P):
                break 
        return P, Q
    
    def update_key(self):
        # Prime generation is expensive, so we'll just update d and e instead ^w^
        self.private['d'] ^= int.from_bytes(hashlib.sha512((str(self.private['d']) + str(time.time())).encode()).digest(), 'big')
        self.private['d'] %= self.private['f']
        self.public['e'] = inverse(self.private['d'], self.private['f'])
        
    def encrypt(self, m_int):
        c_lst = []
        while m_int:
            c_lst += [pow(m_int, self.public['e'], self.public['n'])]
            m_int //= self.public['n']
        return c_lst
    
    def decrypt(self, c_int):
        m_lst = []
        while c_int:
            m_lst += [pow(c_int, self.private['d'], self.public['n'])]
            c_int //= self.public['n']
        return m_lst


# Challenge setup
print("""|
|  ~ Welcome to URSA decryption services
|    Press enter to start key generation...""")

input("|")

print("""|
|    Please hold on while we generate your primes...
|\n|""")
    
oracle = URSA(256, 12)
print("|  ~ You are connected to an URSA-256-12 service, public key ::")
print("|    id = {}".format(hashlib.sha256(str(oracle.public['n']).encode()).hexdigest()))
print("|    e  = {}".format(oracle.public['e']))

print("|\n|  ~ Here is a free flag sample, enjoy ::")
for i in oracle.encrypt(int.from_bytes(FLAG, 'big')):
    print("|    {}".format(i))


MENU = """|
|  ~ Menu (key updated after {} requests)::
|    [E]ncrypt
|    [D]ecrypt
|    [U]pdate key
|    [Q]uit
|"""

# Server loop
CYCLE = 0
while True:
    
    try:

        if CYCLE % 4:
            print(MENU.format(4 - CYCLE))
            choice = input("|  > ")

        else:
            choice = 'u'
        
        if choice.lower() == 'e':
            msg = int(input("|\n|  > (int) "))

            print("|\n|  ~ Encryption ::")
            for i in oracle.encrypt(msg):
                print("|    {}".format(i))

        elif choice.lower() == 'd':
            cip = int(input("|\n|  > (int) "))

            print("|\n|  ~ Decryption ::")
            for i in oracle.decrypt(cip):
                print("|    {}".format(i))
            
        elif choice.lower() == 'u':
            oracle.update_key()
            print("|\n|  ~ Key updated succesfully ::")
            print("|    id = {}".format(hashlib.sha256(str(oracle.public['n']).encode()).hexdigest()))
            print("|    e  = {}".format(oracle.public['e']))

            CYCLE = 0
            
        elif choice.lower() == 'q':
            print("|\n|  ~ Closing services...\n|")
            break
            
        else:
            print("|\n|  ~ ERROR - Unknown command")

        CYCLE += 1
        
    except KeyboardInterrupt:
        print("\n|  ~ Closing services...\n|")
        break
        
    except:
        print("|\n|  ~ Please do NOT abuse our services.\n|")
