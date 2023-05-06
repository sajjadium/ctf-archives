#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Util.number import getPrime, inverse
from secrets import randbelow

# Local imports
with open("flag.txt",'rb') as f:
    FLAG = f.read().decode()
    f.close()

# Just for you sanity
assert len(FLAG) > 64


HDR = r"""|
|   __________     ___   _____  .___  ___     /\  ________  
|   \______   \   /  /  /  _  \ |   | \  \   /  \ \_____  \ 
|    |     ___/  /  /  /  /_\  \|   |  \  \  \/\/   _(__  < 
|    |    |     (  (  /    |    \   |   )  )       /       \
|    |____|      \  \ \____|__  /___|  /  /       /______  /
|                 \__\        \/      /__/               \/
|"""

MENU = r"""|
|  MENU:
|   [E]ncrypt
|   [D]ecrypt
|   [Q]uit
|"""


class Paiaiai:
    """ My first Paillier implementation! So proud of it. ^ w ^ """

    def __init__(self):
        # Key generation
        p, q = [getPrime(512) for _ in range(2)]
        n = p * q
        # Public key
        self.pub = {
            'n'  : n,
            'gp' : pow(randbelow(n**2), p, n**2),
            'gq' : pow(randbelow(n**2), q, n**2)
        }
        # Private key
        self.priv = {
            'la' : (p - 1)*(q - 1),
            'mu' : inverse((pow(self.pub['gp'] * self.pub['gq'], (p-1)*(q-1), n**2) - 1) // n, n)
        }
        
    def encrypt(self, m: str):
        m_int = int.from_bytes(m.encode(), 'big')
        g = pow([self.pub['gp'],self.pub['gq']][randbelow(2)], m_int, self.pub['n']**2)
        r = pow(randbelow(self.pub['n']), self.pub['n'], self.pub['n']**2)
        return (g * r) % self.pub['n']**2
    
    def decrypt(self, c: int):
        cl = (pow(c, self.priv['la'], self.pub['n']**2) - 1) // self.pub['n']
        return (cl * self.priv['mu']) % self.pub['n']

    
print(HDR)
pai = Paiaiai()

while True:
    
    try:
        
        print(MENU)
        choice = input("|  >>> ").lower().strip()
        
        if choice == 'e':
            print("|\n|  ENCRYPT:")
            print("|   [F]lag")
            print("|   [M]essage")
            subchoice = input("|\n|  >>> ").lower().strip()
            
            if subchoice == 'f':
                enc_flag = pai.encrypt(FLAG)
                print("|\n|  FLAG:", enc_flag)
                
            elif subchoice == 'm':
                msg = input("|\n|  MSG: str\n|   > ")
                cip = pai.encrypt(msg)
                print("|\n|  CIP:", cip)
            
        elif choice == 'd':
            cip = input("|\n|  CIP: int\n|   > ")
            msg = pai.decrypt(int(cip))
            print("|\n|  MSG:", msg)
            
        elif choice == 'q':
            print("|\n|  Bai ~ \n|")
            break
            
        else:
            print("|\n|  Trai again ~ \n|")
        
    except KeyboardInterrupt:
        print("\n|\n|  Bai ~ \n|")
        break
        
    except:
        print("|\n|  Aiaiai ~ \n|")
