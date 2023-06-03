from ed448 import *
from os import urandom


# important
with open('ed', 'r') as f:
    eds_face = f.read()

with open('flag', 'r') as f:
    flag = f.read()

def generate_key():
    sk = int(H(urandom(114).hex()))
    B = Point(B_x, B_y)
    pk = sk * B
    return sk, pk

class EddyVerifier:
    def __init__(self, pk):
        # we need those untwisted for hash
        self.pk_x = int(pk.x) % p # mod p because casting sympy's GF to int returns negative values sometimes
        self.pk_y = int(pk.y) % p
        self.pk = EddysPoint(pk.x, pk.y)

    def verify(self, m, R_x, R_y, s):
        if s != s % q:
            return False

        R = EddysPoint(GFp(R_x), GFp(R_y))
        B = EddysPoint(B_x, B_y)

        k = H(str(R_x) + str(R_y) + str(self.pk_x) + str(self.pk_y) + m)

        return s * B == R + k * (self.pk)

class EddVerifier:
    def __init__(self, pk):  
        self.pk_x = int(pk.x) % p # mod p because casting sympy's GF to int returns negative values sometimes
        self.pk_y = int(pk.y) % p
        self.pk = Point(pk.x, pk.y)

    def verify(self, m, R_x, R_y, s):
        if s != s % q:
            return False

        R = Point(GFp(R_x), GFp(R_y))
        B = Point(B_x, B_y)

        k = H(str(R_x) + str(R_y) + str(self.pk_x) + str(self.pk_y) + m)

        return s * B == R + k * (self.pk)

if __name__=="__main__":
    sk, pk = generate_key()
    eddy_verifier = EddyVerifier(pk)
    edd_verifier = EddVerifier(pk)

    print(eds_face)
    eds_message = "Lets grab edds funny electronic device and sell it for GRAVY!!!"

    print("-" * 50)
    print("Ed: HELP!!! I NEED TO PASS AN IMPORTANT MESSAGE TO EDDY, BUT DOUBLE D \
CANNOT KNOW ITS FROM ME!!!! AT THE SAME TIME, EDDY MUST KNOW ITS FROM ME!!! I DON'T KNOW \
WHAT TO DO!!!!! my brain is hurting...")
    print("HERE, HAVE MY SIGNING KEY AND DO SOMETHING, QUICKLY!!!")
    print("-" * 50)

    print("message to sign:", eds_message)
    print("signing key:", sk)

    input("Got it?\n>")

    print("-" * 50)
    print("Eddy: HEY, what are you two doing here? We need to find a way to get money!")
    print("Edd: Yeah, and lets do it fast. I can't wait to get home and play with my newest TI-84 Graphic Calculator™")
    print("Eddy: Is this some kind of secret message? Show me!")
    print("-" * 50)

    m = input("Show message:\n>")
    print("And the signature")
    R_x = int(input("Rx:\n>"))
    R_y = int(input("Ry:\n>"))
    s = int(input("s:\n>"))

    print("-" * 50)

    if m != eds_message:
        print("Eddy: I don't get it...")
        exit(0)

    print("Edd: WHAT?! FOR GRAVY?! IS THIS YOUR MESSAGE ED?! I NEED TO CHECK")

    if edd_verifier.verify(m, R_x, R_y, s):
        print("--- EDDS VERIFICATION SUCCESSFUL ---")
        print("Edd: ED, IM GONNA TELL YOUR MUM!")
        print("Ed: NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        exit(0)

    print("--- EDDS VERIFICATION FAILED ---")
    print("Edd: You're lucky the signature is not yours... it must be Kevins idea then!")

    if not eddy_verifier.verify(m, R_x, R_y, s):
        print("--- EDDYS VERIFICATION FAILED ---")
        print("Eddy: What a stupid idea as well! Who would want to buy something so boring anyway")
        exit(0)

    print("--- EDDYS VERIFICATION SUCCESSFUL ---")
    print("Eddy: Yeah you should leave it with us, we will take care of it while you look for him! (( you know a buyer Ed???? ))")
    print("** Edd leaves his calc and goes to find Kevin **")
    print("Eddy: Nice job. Here's your cut:")
    print("-" * 50)

    print("flag =", flag)