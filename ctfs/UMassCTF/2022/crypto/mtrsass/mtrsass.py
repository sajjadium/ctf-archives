#!/usr/local/bin/python
#
# Polymero
#

# Imports
from Crypto.Util.number import long_to_bytes, bytes_to_long, getPrime, inverse
from base64 import urlsafe_b64encode, urlsafe_b64decode
from hashlib import sha256
import json

# Local imports
with open("flag.txt",'rb') as f:
    FLAG = f.read().decode()
    f.close()

# Helper functions
def b64enc(x):
    return urlsafe_b64encode(x).decode().rstrip("=")

def b64dec(x):
    return urlsafe_b64decode(x + "===")


HDR = r"""|
|   ___  ______________  _____  ___   _____ _____ 
|   |  \/  |_   _| ___ \/  ___|/ _ \ /  ___/  ___|
|   | .  . | | | | |_/ /\ `--./ /_\ \\ `--.\ `--. 
|   | |\/| | | | |    /  `--. \  _  | `--. \`--. \
|   | |  | | | | | |\ \ /\__/ / | | |/\__/ /\__/ /
|   \_|  |_/ \_/ \_| \_|\____/\_| |_/\____/\____/ 
|"""


class RSASSkey:
    """ RSA Signature Scheme """
    def __init__(self):
        # RSA key generation
        while True:
            p,q = [getPrime(512) for _ in range(2)]
            if (p % 0x10001) and (q % 0x10001):
                break
        # Public key
        self.pub = {
            "n" : p * q,
            "e" : 0x10001
        }
        # Private key
        self.priv = {
            "p" : p,
            "q" : q,
            "d" : inverse(0x10001, (p-1)*(q-1))
        }
        
    def __repr__(self):
        return "RSASS"
    
    def sign(self, message: str):
        """ Returns RSA-SHA256 signature of a given message string. """
        msg_hash = int(sha256(message.encode()).hexdigest(),16)
        return long_to_bytes(pow(msg_hash, self.priv["d"], self.pub["n"]))
    
    def verify(self, sign_obj: dict):
        """ Verifies RSA-SHA256 signature object. """
        msg_hash = int(sha256(sign_obj["msg"].encode()).hexdigest(),16)
        pubint = bytes_to_long(b64dec(sign_obj["pub"]))
        sigint = bytes_to_long(b64dec(sign_obj["sig"]))
        if pow(sigint, 0x10001, pubint) == msg_hash:
            return True, None
        else:
            return False, "Verify ERROR -- Invalid signature."
        
        
class Meert:
    """ Merkle Tree Signatures """
    def __init__(self, depth, signer):
        self.signer = signer
        if (depth < 1) or (depth > 8):
            raise ValueError("Let's be serious for a bit, okay?")
            
        self.keys = [self.signer() for _ in range(2**depth)]
        
        self.tree = [[sha256(long_to_bytes(i.pub["n"])).digest() for i in self.keys]]
        while len(self.tree[-1]) > 1:
            self.tree += [[sha256(b"".join(self.tree[-1][i:i+2])).digest() for i in range(0,len(self.tree[-1]),2)]]
            
        self.root = self.tree[-1][-1]
        
    def __repr__(self):
        return "{}-{}-MT ({} keys left) w/ ROOT: {}".format(len(self.tree) - 1, self.signer.__name__, len(self.keys), b64enc(self.root))
    
    def sign(self, message: str):
        if not self.keys:
            raise ValueError("No more keys...")
        signer = self.keys.pop(0)
        auth_id = (len(self.tree[0]) - len(self.keys)) - 1
        auth_path = b"".join([bytes([(auth_id >> i) & 1]) + self.tree[i][(auth_id >> i) ^ 1] for i in range(len(self.tree) - 1)])
        return {
            "msg" : message,
            "sig" : b64enc(signer.sign(message)),
            "pub" : b64enc(long_to_bytes(signer.pub["n"])),
            "nap" : b64enc(auth_path)
        }
    
    def verify(self, sign_obj: dict):
        valid, error = RSASSkey.verify(None, sign_obj)
        if not valid:
            return False, error
        auth_byte = b64dec(sign_obj["nap"])
        auth_list = [auth_byte[i:i+33] for i in range(0,len(auth_byte),33)]
        auth_hash = sha256(b64dec(sign_obj["pub"])).digest()
        for i in auth_list:
            auth_hash = sha256(i[1:]*(i[0]) + auth_hash + i[1:]*(i[0] ^ 1)).digest()
        if auth_hash != self.root:
            return False, "Verify ERROR -- Inauthentic signature."
        return True, None


print(HDR)
meert = Meert(3, RSASSkey)


while True:

    try:

        print("|\n|  MENU:")
        print("|   [S]ign")
        print("|   [V]erify")
        print("|   [Q]uit")

        choice = input("|\n|  >> ")

        if choice.lower() == 's':
            print("|\n|  MSG: str")
            msg = input("|   > ")

            if 'flag' in msg.lower():
                print("|\n|   No sneaky business here, okay? \n|")

            else:
                sig = meert.sign(msg)
                print("|\n|  SIG:", json.dumps(sig))

        elif choice.lower() == 'v':
            print("|\n|  SIG: json")
            sig = json.loads(input("|   > "))
            success, error = meert.verify(sig)

            if success:
                if sig["msg"] == "gib flag pls":
                    print("|\n|   Alright, alright... Here you go: {}".format(FLAG))
                else:
                    print("|\n|   Signature successfully verified. I told you it would work...")

            else:
                print("|   {}".format(error))

        elif choice.lower() == 'q':
            raise KeyboardInterrupt()

        else:
            print("|\n|   Excuse me, what? \n|")

    except KeyboardInterrupt:
        print("\n|\n|   Ciao ~ \n|")
        break

    except:
        print("|\n|   Errr ~ \n|")