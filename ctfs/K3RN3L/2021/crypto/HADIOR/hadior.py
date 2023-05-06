#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Util.number import inverse, getPrime, isPrime
from secrets import randbelow
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256
import json, os, time

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()

HDR = r"""| 
|         Security provided by HADIOR     
|                          _             
|      _     _____________( )__________  
|     | |   (_____________   _________ \ 
|     | |___________     _| |    _____) )
|     |  ___   ___  |   /   |   |  __  / 
|     | |   | |   | |__/ /| |___| |  \ \ 
|     |_|   |_|   |_____/  \_____/    \_\
|
|          HADIOR will hold the DOOR     
|"""

MENU = r"""|
|
|  [G]enerate user token
|  [R]equest access
|"""

def legendre_symbol(a, p):
    ls = pow(a, (p - 1) // 2, p)
    return -1 if ls == p - 1 else ls

def modular_sqrt(a, p):
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)
    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e
    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)
        if m == 0:
            return x
        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m


class HADIOR:
    """ HADIOR will hold the DOOR. """

    def __init__(self, bits=512):
        # Generate *field with large prime order
        self.q = 0
        while not self.q:
            self.p = getPrime(bits)
            for k in range(2,128+1):
                if (self.p-1) % k == 0 and isPrime((self.p-1)//k):
                    self.q = (self.p-1) // k
                    self.g = pow(2,k,self.p)
        # Generate keys
        self.sk = randbelow(self.q)
        self.pk = pow(self.g, self.sk, self.p)
    
    def tokenify(self, data):
      
        out = []
        for i in data:                
            try:
                if type(i) == int:
                    j = i.to_bytes((i.bit_length()+7)//8,'big')
                    out += [urlsafe_b64encode(j).decode()[:(len(j)*8+5)//6]]
                else:
                    out += [urlsafe_b64encode(i).decode()[:(len(i)*8+5)//6]]
            except:
                pass
        return '.'.join(out)
        
    def __repr__(self):
        return 'Domain parameters ' + self.tokenify([self.g,self.p])
    
    # Signatures
    def d(self, x):
        if type(x) == bytes:
            x = int.from_bytes(x,'big')
        x %= self.p
        return sum([int(i) for i in list('{:0512b}'.format(x ^ self.sk))])
    
    def h(self, x):
        if type(x) == int:
            x = x.to_bytes((x.bit_length()+7)//8,'big')
        return int.from_bytes(sha256(x).digest(),'big')
    
    def sign(self, m):
        k = randbelow(self.q)
        r = pow(self.g,k,self.p) % self.q
        s = pow( inverse(k,self.q) * (self.h(m) + self.sk * r), self.d(m), self.q)
        return r,s
    
    def verify(self, m, r, s):
        h = self.h(m)
        d = self.d(m)
        if d % 2:
            s = pow(s, inverse(d, self.q-1), self.q)
            u = inverse(s, self.q)
            v = ( h * u ) % self.q
            w = ( r * u ) % self.q
            return r == ( ( pow(self.g,v,self.p) * pow(self.pk,w,self.p) ) % self.p ) % self.q
        else:
            lst = []
            for si in [modular_sqrt(s, self.q), (-modular_sqrt(s, self.q))%self.q]:
                sj = pow(si, inverse(d, self.q-1), self.q)
                u = inverse(sj, self.q)
                v = ( h * u ) % self.q
                w = ( r * u ) % self.q
                lst += [r == ( ( pow(self.g,v,self.p) * pow(self.pk,w,self.p) ) % self.p ) % self.q]
            return any(lst)
        
    # Cookies!
    def bake(self, username, admin=False):
        while True:
            salt = os.urandom(4).hex()
            data = json.dumps({'user' : username, 'admin' : admin, 'salt' : salt}).encode()
            db64 = urlsafe_b64encode(data)[:(len(data)*8+5)//6]
            tb64 = urlsafe_b64encode(int(time.time()).to_bytes(4,'big'))[:-2]
            cb64 = db64 + b'.' + tb64
            r, s = self.sign(cb64)
            if self.verify(cb64, r, s):
                return cb64.decode() + '.' + self.tokenify([r, s])
        
    def inspect(self, cookie):
        data, t, r, s = cookie.split('.')
        r = int.from_bytes(urlsafe_b64decode(r + '==='),'big')
        s = int.from_bytes(urlsafe_b64decode(s + '==='),'big')
        if not self.verify((data + '.' + t).encode(), r, s):
            return 'INSPECT ERROR -- Invalid cookie.'
        try:
            data = json.loads(urlsafe_b64decode(data + '===').decode())
        except:
            return 'INSPECT ERROR -- Broken cookie.'
        return data


# Challenge
print(HDR)

print('|  ' + 'Establishing connection...', end='\r', flush=True)

t0 = time.time()
hadior = HADIOR()
t1 = time.time()

print('|  ' + 'Connection established in {:.2f} s.'.format(t1-t0))
print('|\n|  ' + str(hadior))

while True:

    try:

        print(MENU)

        choice = input('|  >> ')

        if choice.lower() == 'g':

            username = input('|\n|  Username: ')

            cookie = hadior.bake(username=username)

            print('|\n|  Token: ' + cookie)

        elif choice.lower() == 'r':

            cookie = input('|\n|  User token: ')

            try:

                inspect = hadior.inspect(cookie)

            except:

                print('|\n|   HADIOR ERROR -- Invalid input.')
                continue

            if type(inspect) == dict:

                if 'admin' in inspect and 'user' in inspect:

                    if inspect['admin'] is True:

                        print('|\n|\n|    WELCOME admin {}.'.format(inspect['user']))
                        print('|\n|  There is 1 new message for you.')
                        print('|\n|     From: Polymero')
                        print('|   Congrats! Here is a little gift from me - {}'.format(FLAG.decode()))

                        _ = input('|\n|\n|  Press enter to log out...')

                    else:

                        print('|\n|\n|    WELCOME user {}.'.format(inspect['user']))
                        print('|\n|  There are no new messages for you.')

                        _ = input('|\n|\n|  Press enter to log out...')

                else:

                    print('|\n|  HADIOR ERROR -- Invalid user token.')

            else:

                print('|\n|   ' + inspect)

    except KeyboardInterrupt:

        print('\n|\n|   ~ The DOOR remains secured.\n|')
        break

    except:

        print('|\n|   HADIOR ERROR -- Unexpected error, please contact a service admin.\n|')
