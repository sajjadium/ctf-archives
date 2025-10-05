from sage.all import *
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from fastecdsa.curve import P256 as EC
from fastecdsa.point import Point
import os, random, hashlib, json

load('secret.sage')

class SecureSignService:
    def __init__(self):
        self.G = Point(EC.gx, EC.gy, curve=EC)
        self.order = EC.q
        self.p = EC.p
        self.a = EC.a
        self.b = EC.b
        self.privkey = random.randrange(1, self.order - 1)
        self.pubkey = (self.privkey * self.G)
        self.key = os.urandom(16)
        self.iv = os.urandom(16)

    def split_privkey(self, privkey):
        shares = []
        coeffs = [privkey]
        for _ in range(3):
            coeffs.append(random.randrange(1, self.order))

        P.<x> = PolynomialRing(GF(self.order))
        poly = sum(c*x^i for i, c in enumerate(coeffs))

        for x in range(1, 5):
            y = poly(x=x)
            shares.append((x, y))
        return shares

    def reconstruct_privkey(self, shares):
        P.<x> = PolynomialRing(GF(self.order))
        reconst_poly = P.lagrange_polynomial(shares)
        return int(reconst_poly(0))

    def shares_encrypt(self, shares):
        return [self.aes_encrypt(long_to_bytes(int(s[1]))).hex() for s in shares]

    def shares_decrypt(self, shares):
        return [(x+1, bytes_to_long(self.aes_decrypt(bytes.fromhex(y)))) for x, y in enumerate(shares)]

    def generate_key(self):
        self.privkey = random.randrange(1, self.order - 1)
        self.pubkey = (self.privkey * self.G)

    def ecdsa_sign(self, message, privkey):
        z = int(hashlib.sha256(message).hexdigest(), 16)
        k = random.randrange(1, self.order - 1)
        r = (k*self.G).x % self.order
        s = (inverse(k, self.order) * (z + r*privkey)) % self.order
        return (r, s)

    def ecdsa_verify(self, message, r, s, pubkey):
        r %= self.order
        s %= self.order
        if s == 0 or r == 0:
            return False
        z = int(hashlib.sha256(message).hexdigest(), 16)
        s_inv = inverse(s, self.order)
        u1 = (z*s_inv) % self.order
        u2 = (r*s_inv) % self.order
        W = u1*self.G + u2*pubkey
        return W.x == r

    def aes_encrypt(self, plaintext):
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.iv)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext)
        return tag + ciphertext

    def aes_decrypt(self, ciphertext):
        tag, ct = ciphertext[:16], ciphertext[16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.iv)
        plaintext = cipher.decrypt_and_verify(ct, tag)
        return plaintext

    def get_flag(self):
        key = hashlib.sha256(long_to_bytes(self.privkey)).digest()[:16]
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_flag = cipher.encrypt(pad(FLAG.encode(), 16))
        return encrypted_flag


if __name__ == '__main__':
    print("Welcome to Fl0pper Zer1 – Secure Signing Service!\n")

    S = SecureSignService()

    signkey = S.shares_encrypt(S.split_privkey(S.privkey))

    print(f"Here are your encrypted signing key shares, use them to sign a message : {json.dumps({'pubkey': {'x': hex(S.pubkey.x), 'y': hex(S.pubkey.y)}, 'signkey': signkey})}")
    
    while True:
        print("\nOptions:\n \
    1) sign <message> <signkey> : Sign a message\n \
    2) verify <message> <signature> <pubkey> : Verify the signed message\n \
    3) generate_key : Generate new signing key shares\n \
    4) get_flag : Get the flag\n \
    5) quit : Quit\n")

        try:
            inp = json.loads(input('> '))

            if 'option' not in inp:
                print(json.dumps({'error': 'You must send an option'}))

            elif inp['option'] == 'sign':
                msg = bytes.fromhex(inp['msg'])
                signkey = inp['signkey']
                sk = S.reconstruct_privkey(S.shares_decrypt(signkey))

                r, s = S.ecdsa_sign(msg, sk)
                print(json.dumps({'r': hex(r), 's': hex(s)}))

            elif inp['option'] == 'verify':
                msg = bytes.fromhex(inp['msg'])
                r = int(inp['r'], 16)
                s = int(inp['s'], 16)
                px = int(inp['px'], 16)
                py = int(inp['py'], 16)
                pub = Point(px, py, curve=EC)

                verified = S.ecdsa_verify(msg, r, s, pub)

                if verified:
                    print(json.dumps({'result': 'Success'}))
                else:
                    print(json.dumps({'result': 'Invalid signature'}))

            elif inp['option'] == 'generate_key':
                S.generate_key()
                signkey = S.shares_encrypt(S.split_privkey(S.privkey))
                print("Here are your *NEW* encrypted signing key shares :")
                print(json.dumps({'pubkey': {'x': hex(S.pubkey.x), 'y': hex(S.pubkey.y)}, 'signkey': signkey}))

            elif inp['option'] == 'get_flag':
                encrypted_flag = S.get_flag()
                print(json.dumps({'flag': encrypted_flag.hex()}))

            elif inp['option'] == 'quit':
                print("Adios :)")
                break

            else:
                print(json.dumps({'error': 'Invalid option'}))
        
        except Exception as e:
            print(json.dumps({'error': 'Oops! Something went wrong'}))
            break

