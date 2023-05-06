#!/usr/bin/python3

import hashlib
import hmac
import sys
from base64 import b64encode, b64decode
from Crypto import Random
from Crypto.Cipher import AES

key = open('./key', 'r').read().strip().encode()
flag = open('./flag.txt', 'r').readline().strip().encode()


def get_hmac(m):
    return hmac.new(key, msg=m, digestmod=hashlib.sha256).digest()


def hmac_is_valid(pt):
    digest = pt[-32:]
    msg = pt[:-32]
    return equal_bytearrays(hmac.new(key, msg=msg, digestmod=hashlib.sha256).digest(), digest)


def equal_bytearrays(a1, a2):
    if len(a1) != len(a2):
        return False
    else:
        for i in range(len(a1)):
            if a1[i] != a2[i]:
                return False
        return True


def pad(pt):
    pad_value = 16 - len(pt) % 16
    pt = pt + (chr(pad_value) * pad_value).encode()
    return pt


def verify_padding_and_unpad(pt):
    pad_value = pt[-1]
    if pad_value == 0 or pad_value > 32:
        return False
    else:
        pt = pt[:(-1 * pad_value)]
        return pad_value, pt


def encrypt(pt):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pt)
    ct = iv + ct
    ct = b64encode(ct)
    return ct



def decrypt(ct):
    ct_incl_iv = b64decode(ct)
    iv, ct = ct_incl_iv[:16], ct_incl_iv[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.decrypt(ct)


def decrypt_and_verify(ct):
    pt = decrypt(ct)
    pad, pt = verify_padding_and_unpad(pt)
    if pt and hmac_is_valid(pt):
        print(
            "\nValid plaintext. We assume you have purchased our flag decryption key and can therefore read the flag. Thank you for your patronage.\n")

        return True
    print("Something went wrong during decryption. Try again?")
    return False


def get_canine_order():
    print("What type of canine would you like to purchase?")
    print("> ", end="")
    canine_type = input().encode()
    print("\nHow many would you like to purchase? (We have unlimited supplies...)")
    print("> ", end="")
    canine_quant = input().encode()
    return canine_type, canine_quant


def process_encryption():
    canine_type, canine_order = get_canine_order()

    msg = b"Congratulations, you just completed your " + canine_type + b" purchase instead of buying this beautiful flag: " + flag
    msg += b". What were you thinking? Fortunately you have helped " + canine_order + b" canines and puppies find homes"
    hmac = get_hmac(msg)
    pt = msg + hmac
    pt = pad(pt)
    ct = encrypt(pt)
    print()
    print(b"A plane flies overhead flying a banner that reads: " + ct, "\n")
    return ct


def get_selection():
    print("Enter your selection:")
    print("   1) Enter the shop")
    print("   2) Decrypt")
    print("   3) Leave the shop\n")
    print("> ", end='')
    selection = input().strip()
    if selection in list('123'):
        print("")
        return selection
    else:
        print("Error: Invalid selection.")
        exit(0)


def main():
    print("**********      C S A W   G I F T   S H O P      **********\n")
    print("   Welcome to the CSAW Canine Gift Shop!    ")
    print("Leaving city dwellers have asked us to find home for their MANY canine friends.")
    print("We have canines of all kinds ... as well as encrypted flags constantly flying ")
    print("overhead and a key to decrypt them that should be well within your price range.\n\n")

    while (1):
        selection = int(get_selection())
        try:
            if selection == 1:
                process_encryption()
                sys.stdout.flush()
            elif selection == 2:
                print("Enter the base64-encoded ciphertext to decrypt: ")
                print("> ", end='')
                ct = input().encode()
                decrypt_and_verify(ct)
                sys.stdout.flush()
            elif selection == 3:
                print("Thank you for shopping with CSAW!")
                exit(0)
            else:
                print("Error: invalid menu option.")
                raise Exception
        except Exception as ex:
            print("\nSomething went wrong......try again?\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
