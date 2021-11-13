#!/usr/bin/env python3
#
# Polymero
#

# Imports
import hashlib, secrets, json
from Crypto.PublicKey import DSA

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read()
    f.close()


class CCC:
    """ Certified Certificate Certifier. (It's just DSA...) """
    
    def __init__(self, p, q, g):
        """ Initialise class object. """
        self.p = p
        self.q = q
        self.g = g
        
        self.sk = secrets.randbelow(self.q)
        self.pk = pow(self.g, self.sk, self.p)
        
    def inv(self, x, p):
        """ Return modular multiplicative inverse over prime field. """
        return pow(x, p-2, p)
        
    def H_int(self, m):
        """ Return integer hash of byte message. """
        return int.from_bytes(hashlib.sha256(m).digest(),'big')
    
    def bake(self, m, r, s):
        """ Return JSON object of signed message. """
        return json.dumps({ 'm' : m.hex() , 'r' : r , 's' : s })
        
    def sign(self, m):
        """ Sign a message. """
        h = self.H_int(m)
        k = secrets.randbelow(self.q)
        r = pow(self.g, k, self.p) % self.q
        s = ( self.inv(k, self.q) * (h + self.sk * r) ) % self.q
        assert self.verify_recv(m, r, s, self.pk)
        return self.bake(m, r, s)
        
    def verify_recv(self, m, r, s, pk):
        """ Verify a message received from pk holder. """
        if r < 2 or r > self.q-2 or s < 2 or s > self.q-1:
            return False
        h = self.H_int(m)
        u = self.inv(s, self.q)
        v = (h * u) % self.q
        w = (r * u) % self.q
        return r == ((pow(self.g,v,self.p) * pow(pk,w,self.p)) % self.p) % self.q




#------------------------------------------------------------------------------------------------------------
# SERVER CODE
#------------------------------------------------------------------------------------------------------------

HDR = r"""|
|     ___   ____    ____    ___     __  ______  ____   ___   ____   __ 
|    /   \ |    \  |    |  /  _]   /  ]|      ||    | /   \ |    \ |  |
|   |     ||  o  ) |__  | /  [_   /  / |      | |  | |     ||  _  ||  |
|   |  O  ||     | __|  ||    _] /  /  |_|  |_| |  | |  O  ||  |  ||__|
|   |     ||  O  |/  |  ||   [_ /   \_   |  |   |  | |     ||  |  | __ 
|   |     ||     |\  `  ||     |\     |  |  |   |  | |     ||  |  ||  |
|    \___/ |_____| \____||_____| \____|  |__|  |____| \___/ |__|__||__|
|"""

MENU = r"""|
|  Domain Controller options:
|   [G]enerate new domain parameters
|   [P]rovide domain parameters
|
|  Network options:
|   [S]end signed message to Harry
|"""

print(HDR)

# Set up domain
domain = DSA.generate(1024)
P,Q = domain.p, domain.q
G_default = domain.g

# Set up static clients
Auth1 = None
Auth2 = None
Harry = None

# Set win conditions
WIN1 = False
WIN2 = False

print('|  Current domain parameters:')
print('|   P =',P)
print('|   Q =',Q)
print('|   G (default) =',G_default)
print('|')

while True:
    
    if WIN1 and WIN2:
        
        print('|\n|  Objection!!!\n|  You have done it! Harry will hopefully never hoard again... {}'.format(FLAG))
        break

    print(MENU)
    
    try:
        
        choice = input('|  >> ').lower()
        
        if choice == 'g':
            
            domain = DSA.generate(1024)
            P, Q = domain.p, domain.q
            G_default = domain.g
            
            print('|\n|  Current domain parameters:')
            print('|   P =',P)
            print('|   Q =',Q)
            print('|   G (default) =',G_default)
            print('|')
            
        elif choice == 'p':

            # Reset win conditions
            WIN1 = False
            WIN2 = False
            
            print('|\n|  [1] Authenticator Alice')
            print('|  [2] Certifier Carlo')
            print('|  [3] Harry the Flag Hoarder')
            
            target = input('|\n|  >> Target: ')

            try:

                G_user = int(input('|  >> G_user (empty for default): '))

            except:

                G_user = G_default

            if G_user < 2 or G_user > P-2:
                print('|\n|  USER INPUT ERROR -- A valid generator is within the range {2 ... Q-2}.')
                continue

            if pow(G_user,Q,P) != 1:
                print('|\n|  USER INPUT ERROR -- A valid generator has order Q.')
                continue
            
            if target == '1':             

                Auth1 = CCC(P,Q,G_user)
                print("|\n|  Authenticator Alice's public key: {}".format(Auth1.pk))
                
            elif target == '2':

                Auth2 = CCC(P,Q,G_user)
                print("|\n|  Certifier Carlo's public key: {}".format(Auth2.pk))

                
            elif target == '3':

                Harry = CCC(P,Q,G_user)
                print("|\n|  Harry's public key: {}".format(Harry.pk))

            else:
                
                print('|\n|  USER INPUT ERROR -- Unknown target.')
            
        elif choice == 's':
            
            try:
                
                signed_msg = input('|\n|  JSON object (m,r,s,pk): ')
                
                jsonobject = json.loads(signed_msg)
                
                if Harry.verify_recv(jsonobject['m'],jsonobject['r'],jsonobject['s'],jsonobject['pk']):
                    
                    if jsonobject['m'] == b'I, Authenticator Alice, do not concur with the hoarding of flags.'.hex() and jsonobject['pk'] == Auth1.pk:
                        
                        WIN1 = True
                            
                    elif jsonobject['m'] == b'I, Certifier Carlo, do not concur with the hoarding of flags.'.hex() and jsonobject['pk'] == Auth2.pk:
                        
                        WIN2 = True
                        
                    print('|\n|  Your message was delivered succesfully.')
                        
                else:
                    
                    print('|\n|  VERIFICATION ERROR -- Message was rejected.')
                
            except:
                
                print('|\n|  USER INPUT ERROR -- Invalid input.')
            
        else:
            
            print('|\n|  USER INPUT ERROR -- Unknown option.')
        
    except KeyboardInterrupt:
        
        print('\n|\n|  ~ OVERRULED!\n|')
        break
        
    except:
        
        print('|\n|  RUN ERROR -- An unknown error has occured.')
