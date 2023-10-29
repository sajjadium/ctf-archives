from secrets import randbelow
from hashlib import sha256
from Crypto.Util.number import long_to_bytes
import os


def H(msg):
    return sha256(msg).digest()


class NZKP:
    def __init__(self):
        self.p = 26758122283288400636617299098044383566046025569206625247969009149087529122945186469955025131558423244906400120599593226103736432404955901283002339947768387  # prime
        self.q = (self.p - 1) // 2  # prime
        self.g = 3
        self.w = randbelow(self.q)
        self.x = pow(self.g, self.w, self.p)

    def encrypt(self, pubkey, flag):
        secretkey = long_to_bytes(pow(pubkey, self.w ** 2, self.p))  # w**2 for doubled protection
        return bytes(a ^ b for a, b in zip(H(secretkey), flag.encode()))

    def ZKPannounce(self):
        u = randbelow(self.q)
        a = pow(self.g, u, self.p)
        return u, a
    
    def ZKPchallenge(self):
        c = randbelow(self.q)
        return c
    
    def ZKPresponse(self, c, u, w):
        return (c * u + w) % self.q
    
    def ZKPverify(self, a, c, r, x):
        return pow(self.g, r, self.p) == (pow(a, c, self.p) * x) % self.p


def main():
    nzkp = NZKP()
    flag = os.getenv("FLAG")
    if not flag:
        print("Did not find flag in env, crashing.")
        exit(1)

    print("--- GREETING ---")
    print("Welcome to the private data vault. You can create a personalized time capsule that will be safe until "
          "big quantum computers are around.\nTo protect against misuse, it employees mutual zero-knowledge "
          "proofs.")
    print("--- PARAMETERS ---")
    print(f"Generator g: {nzkp.g}")
    print(f"Safe prime p: {nzkp.p}")

    while True:
        try:
            nzkp = NZKP()
            print("\n--- NEW SESSION ---")
            print("A new keypair was generated!")
            print(f"Server public key x: {nzkp.x}")

            print("--- KEY EXCHANGE ---")
            # Pub key upload
            upub = int(input("Enter user public key as long int> "))
            y = upub % nzkp.p
            if nzkp.g != y and 0 != y:
                print(f"User public key saved as: {y}")
            else:
                print("Invalid public key!")
                continue

            # User key ZKP
            print("You now have to prove that your public key is valid.")
            a = int(input("Enter user announcement as long int> "))
            c = nzkp.ZKPchallenge()
            print(f"Your challenge is: {c}")
            r = int(input("Enter user response as long int> "))
            r = r % nzkp.q
            if nzkp.ZKPverify(a, c, r, y):
                print("Authentication succeeded!")
            else:
                print("Authentication failed!")
                continue

            # Server key ZKP
            print("The server will now prove that its public key is valid.")
            u, a = nzkp.ZKPannounce()
            print(f"The announcement a is: {a}")

            c = int(input("Enter user challenge c as long int> "))
            c = c % nzkp.q

            r = nzkp.ZKPresponse(c, u, nzkp.w)
            print(f"The response r is: {r}")

            print("You may now verify the knowledge as follows:")
            print("pow(g, r, p) == (pow(a, c, p) * x) % p")

            print("--- FLAG GEN ---")
            print(f"Encrypted flag: {nzkp.encrypt(y, flag).hex()}")
            print("--- END ---")
        except:
            print(f"An error occurred! Restarting...")


if __name__ == "__main__":
    main()
