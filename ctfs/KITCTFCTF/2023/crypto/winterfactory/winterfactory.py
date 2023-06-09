#!/usr/bin/env python3

import winternitz.signatures
import random
from binascii import unhexlify

class factory:

    def __init__(self):

        w = 2**16
        self.wots = winternitz.signatures.WOTS(w, digestsize=256, hashfunction=winternitz.signatures.openssl_sha256)

        self.factory_id = 831347528
        init_message = bytes("surely no secret here"+str(self.factory_id), "utf-8")

        self.certification = self.wots.sign(init_message)

        self.p11 = None
        self.p12 = None
        self.p13 = None
        self.p21 = None
        self.p22 = None
        self.p23 = None

    def produce(self):
        r1 = random.randbytes(16)
        r2 = random.randbytes(16)
        self.p11, self.p12, self.p13 = r1, self.p11, self.p12
        self.p21, self.p22, self.p23 = r2, self.p21, self.p22

    def run_factory(self):

        print(f"You arrive at the factory to buy a new number for your room at home. At the door you read: 'This factory is certified:' followed by these numbers")
        print()
        output_array(self.certification["signature"])
        print()
        print(f"Going inside you see a conveyer belt presenting their newest numbers.")

        while True:
            self.produce()
            self.print_belt()
            answer = input("Do you want to buy one of the current numbers? >> ")
            if answer == "yes":
                self.accept_products()
                exit()

    def accept_products(self):
        choice = int(input("Which number do you want to buy? >> "), 16)

        product_of_choice = self.p11 if choice == 1 else self.p21
        other_product = self.p21 if choice == 1 else self.p11

        product_certification = self.wots.sign(product_of_choice)
        print("You manage to see part of the signature from the customer in front of you:")
        print(product_certification["signature"][-2].hex())

        user_certificate = input("Please sign your order >> ")
        user_certificate = [unhexlify(c) for c in user_certificate.split("|")]

        if self.wots.verify(other_product, user_certificate):
            print("GPNCTF{fake_flag}")


    def print_belt(self):
        print()
        print("="*108)
        s1 = f" | {self.p11.hex()} | "
        s1 += f"{self.p12.hex() if self.p12 != None else ' '*32} | "
        s1 += f"{self.p13.hex() if self.p13 != None else ' '*32} |"
        print(s1)
        print("="*108)
        s2 = f" | {self.p21.hex()} | "
        s2 += f"{self.p22.hex() if self.p22 != None else ' '*32} | "
        s2 += f"{self.p23.hex() if self.p23 != None else ' '*32} |"
        print(s2)
        print("="*108)
        print()



def output_array(arr):
    s = "".join([a.hex()+"|" for a in arr])
    print(s[:-1])


if __name__ == "__main__":
    f = factory()
    f.run_factory()
