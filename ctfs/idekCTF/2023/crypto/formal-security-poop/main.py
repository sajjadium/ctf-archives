from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from ecc import *

class Vault:
    def __init__(self) -> None:
        self.secrets = {}

    def authenticate(self, owner: str) -> None:
        # Please see https://en.wikipedia.org/wiki/Proof_of_knowledge#Schnorr_protocol for how to interact
        # But we do it over ellipthicc curves, because we already have a group setup :D
        P, _ = self.secrets[owner]
        print(f"Please prove that you are {owner}:")

        T = Point.input("Give me the point T: ")
        print('c =', c := randbelow(p))
        s = int(input('s = '))

        if s*G == T + c*P:
            print("Successfully authenticated!")
        else:
            print("Who are you?? Go away!")
            exit()

    def sign(self, owner: str):
        _, secret = self.secrets[owner]
        m = int.from_bytes(sha512(secret).digest(), 'big') % p

        k = randbelow(1 << 64) # [Note to self: make the bound dynamic on Y's order]
        r = (k*G).x
        s = (m + r*y)*pow(k, -1, p) % p
        # Verify the signature with (r, _) == (1/s)*(m*G + r*Y)
        return r, s

    def store(self, secret: bytes, owner: str, P: Point):
        if owner not in self.secrets:
            self.secrets[owner] = P, secret
            return

        self.authenticate(owner)
        self.secrets[owner] = P, secret

    def retrieve(self, owner: str):
        _, secret = self.secrets[owner]
        self.authenticate(owner)
        return secret


def session():
    # x, X = gen_key(): your ephemeral keypair
    X = Point.input("What is your ephemeral key?")
    assert X != E.O

    y, Y = gen_key()
    B.print("Here is my public key:")
    Y.print("Here is my ephemeral key:")

    S = (y + H(Y)*b)*(X + H(X)*A) # Shared knowledge
    return y, Y, sha512(H(S).to_bytes(32, 'big')).digest()[:16]


if __name__ == '__main__':
    with open('flag.txt', 'rb') as f:
        flag = f.read()

    # a, A = gen_key(): your long term keypair
    A = Point.input("What is your public key?")
    b, B = gen_key()
    y, Y, key = session()
    # Communication is encrypted so that third parties can't steal your secrets!
    aes = AES.new(key, AES.MODE_ECB)

    vault = Vault()
    vault.store(flag, 'Bob', B)

    while 1:
        print("""
[1] Store a secret
[2] Retrieve a secret
[3] Sign a secret
[4] Reinitialize session
        """.strip())
        opt = int(input('>>> '))

        if opt == 1:
            owner = input("Who are you? ")
            secret = aes.decrypt(bytes.fromhex(input('secret = ')))
            vault.store(unpad(secret, 16), owner, A)
            print("Secret successfully stored!")

        elif opt == 2:
            owner = input("Who are you? ")
            secret = pad(vault.retrieve(owner), 16)
            print("Here is your secret:")
            print('secret =', aes.encrypt(secret).hex())

        elif opt == 3:
            owner = input("Whose secret should I sign? ")
            r, s = vault.sign(owner)
            print("Here is the signature:")
            print('r =', r)
            print('s =', s)

        elif opt == 4:
            y, Y, key = session()
            aes = AES.new(key, AES.MODE_ECB)

        else:
            print("My secrets are safe forever!", flush=True)
            exit()