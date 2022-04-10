#!/usr/bin/env python3
#
# Polymero
#

# Imports
from Crypto.Util.number import getPrime, inverse, GCD
from secrets import randbelow
import os, hashlib

# Local imports
with open('flag.txt','rb') as f:
    FLAG = f.read().decode().strip()
    f.close()


HDR = r"""|
|     _______    _______    _______    _______       __  ___________  __    _____  ___    _______   
|    /"      \  /"     "|  |   __ "\  /"     "|     /""\("     _   ")|" \  (\"   \|"  \  /" _   "|  
|   |:        |(: ______)  (. |__) :)(: ______)    /    \)__/  \\__/ ||  | |.\\   \    |(: ( \___)  
|   |_____/   ) \/    |    |:  ____/  \/    |     /' /\  \  \\_ /    |:  | |: \.   \\  | \/ \       
|    //      /  // ___)_   (|  /      // ___)_   //  __'  \ |.  |    |.  | |.  \    \. | //  \ ___  
|   |:  __   \ (:      "| /|__/ \    (:      "| /   /  \\  \\:  |    /\  |\|    \    \ |(:   _(  _| 
|   |__|  \___) \_______)(_______)    \_______)(___/    \___)\__|   (__\_|_)\___|\____\) \_______)
|                ______    _______   _______   _______  _____  ___    ________  _______  
|               /    " \  /"     "| /"     "| /"     "|(\"   \|"  \  /"       )/"     "| 
|              // ____  \(: ______)(: ______)(: ______)|.\\   \    |(:   \___/(: ______) 
|             /  /    ) :)\/    |   \/    |   \/    |  |: \.   \\  | \___  \   \/    |   
|            (: (____/ // // ___)   // ___)   // ___)_ |.  \    \. |  __/  \\  // ___)_  
|             \        / (:  (     (:  (     (:      "||    \    \ | /" \   :)(:      "| 
|              \"_____/   \__/      \__/      \_______) \___|\____\)(_______/  \_______) 
|"""

print(HDR)


class RSA_then_Paillier:
    """ Layered Cipher of RSA : Zn -> Zn then Paillier : Zn -> Zn2. """

    def __init__(self, domain: tuple):
        # Class parameters
        P, Q = domain
        self.HISTORY = []

        # RSA public key
        self.E = 0x10001
        self.N = P * Q

        # RSA private key
        F = (P - 1) * (Q - 1)
        self.D = inverse(self.E, F)

        # Paillier public key
        self.G = randbelow(self.N * self.N)

        # Paillier private key
        self.L = F // GCD(P - 1, Q - 1)
        self.U = inverse((pow(self.G, self.L, self.N * self.N) - 1) // self.N, self.N)


    def encrypt(self, msg: int) -> int:
        # RSA
        cip_rsa = pow(msg, self.E, self.N)

        # Paillier
        g_m = pow(self.G, cip_rsa, self.N * self.N)
        r_n = pow(randbelow(self.N), self.N, self.N * self.N)
        cip = (g_m * r_n) % (self.N * self.N)

        # Update HISTORY
        self.HISTORY += [hashlib.sha256(cip.to_bytes(256, 'big')).hexdigest()]
        return cip


    def decrypt(self, cip: int) -> int:
        # Check HISTORY
        if hashlib.sha256(cip.to_bytes(256, 'big')).hexdigest() in self.HISTORY:
            return -1

        # Paillier
        cip_rsa = ((pow(cip, self.L, self.N * self.N) - 1) // self.N * self.U) % self.N

        # RSA
        return pow(cip_rsa, self.D, self.N)


class Paillier_then_RSA:
    """ Layered Cipher of Paillier : Zn -> Zn2 then RSA : Zn2 -> Zn2. """

    def __init__(self, domain: tuple):
        # Class parameters
        P, Q = domain
        self.HISTORY = []

        # RSA public key
        self.E = 0x10001
        self.N = P * Q

        # RSA private key
        F = (P - 1) * (Q - 1) * self.N
        self.D = inverse(self.E, F)

        # Paillier public key
        self.G = randbelow(self.N * self.N)

        # Paillier private key
        self.L = F // GCD(P - 1, Q - 1)
        self.U = inverse((pow(self.G, self.L, self.N * self.N) - 1) // self.N, self.N)


    def encrypt(self, msg: int) -> int:
        # Paillier
        g_m = pow(self.G, msg, self.N * self.N)
        r_n = pow(randbelow(self.N), self.N, self.N * self.N)
        cip_pai = (g_m * r_n) % (self.N * self.N)

        # RSA
        cip = pow(cip_pai, self.E, self.N * self.N)

        # Update HISTORY
        self.HISTORY += [hashlib.sha256(cip.to_bytes(256, 'big')).hexdigest()]
        return cip


    def decrypt(self, cip: int) -> int:
        # Check HISTORY
        if hashlib.sha256(cip.to_bytes(256, 'big')).hexdigest() in self.HISTORY:
            return -1

        # RSA
        cip_pai = pow(cip, self.D, self.N * self.N)

        # Paillier
        return ((pow(cip_pai, self.L, self.N * self.N) - 1) // self.N * self.U) % self.N



DOMAIN = [getPrime(512) for _ in range(2)]

STAGE_1, STAGE_2 = True, False



RTP = RSA_then_Paillier(DOMAIN)
print("|\n|  STAGE 1 :: RSA-then-Paillier\n|\n|   N: {}\n|   G: {}".format(RTP.N, RTP.G))

RTP_PWD = int.from_bytes(os.urandom(32).hex().encode(), 'big')
print("|\n|  RTP(Password): {}".format(RTP.encrypt(RTP_PWD)))

while STAGE_1:

    try:

        print("|\n|\n|  MENU:\n|   [E]ncrypt\n|   [D]ecrypt\n|   [S]ubmit Password")

        choice = input("|\n|  >>> ").lower()


        if choice == 'e':

            user_input = input("|\n|  MSG(int): ")

            print("|\n|  CIP ->", RTP.encrypt(int(user_input)))            


        elif choice == 'd':

            user_input = input("|\n|  CIP(int): ")

            print("|\n|  MSG ->", RTP.decrypt(int(user_input)))    


        elif choice == 's':

            user_input = input("|\n|  PWD(int): ")

            if user_input == str(RTP_PWD):

                print("|\n|\n|  Correct ~ On to Stage 2!\n|")

                STAGE_2 = True
                break

        else:
            print("|\n|  ERROR -- Unknown command.")

    except KeyboardInterrupt:
        print("\n|\n|\n|  Cya ~\n|")
        break

    except:
        print("|\n|  ERROR -- Something went wrong.")


if STAGE_2:

    PTR = Paillier_then_RSA(DOMAIN)
    print("|\n|  STAGE 2 :: Paillier-then-RSA\n|   N: {}\n|   G: {}\n|".format(RTP.N, RTP.G))

    PTR_PWD = int.from_bytes(os.urandom(32).hex().encode(), 'big')
    print("|\n|  PTR(Password): {}".format(PTR.encrypt(PTR_PWD)))

while STAGE_2:

    try:

        print("|\n|\n|  MENU:\n|   [E]ncrypt\n|   [D]ecrypt\n|   [S]ubmit Password")

        choice = input("|\n|  >>> ").lower()


        if choice == 'e':

            user_input = input("|\n|  MSG(int): ")

            print("|\n|  CIP ->", PTR.encrypt(int(user_input)))            


        elif choice == 'd':

            user_input = input("|\n|  CIP(int): ")

            print("|\n|  MSG ->", PTR.decrypt(int(user_input)))    


        elif choice == 's':

            user_input = input("|\n|  PWD(int): ")

            if user_input == str(PTR_PWD):

                print("|\n|\n|  Correct ~ Here's your flag: {}\n|".format(FLAG))

                break

        else:
            print("|\n|  ERROR -- Unknown command.")

    except KeyboardInterrupt:
        print("\n|\n|\n|  Cya ~\n|")
        break

    except:
        print("|\n|  ERROR -- Something went wrong.")
