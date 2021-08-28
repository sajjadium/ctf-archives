#!/usr/bin/env python3.8
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse, getPrime, GCD
import os, hashlib, sys, signal
from time import time
                 
FLAG = "FwordCTF{####################################################################}"

WELCOME = '''
Welcome to CTFCreators Website.
We are a challenges development startup from a team of cybersecurity professionals with diverse backgrounds and skills.'''

server_token = os.urandom(16)
message_to_sign = b"https://twitter.com/CTFCreators"


def H(msg):
    return hashlib.sha256(msg).digest()


def gen_key():
    while True:
        p, q = getPrime(1024), getPrime(1024)
        N = p * q
        e = 65537
        phi = (p - 1) * (q - 1)
        if GCD(e, phi) == 1:
            break
    d = inverse(e, phi)
    pinv = inverse(p, q)
    return N, e, d, pinv


def verify(signature, e, N):
    try:
        signature = int(signature, 16)
        msg = bytes_to_long(message_to_sign)
        verified = pow(signature, e, N)

        if (verified == msg):
            return True
        else:
            return False
    except:
        return False


def sign_up():
    user = str(input("\nUsername : ")).encode()
    proof = b'is_admin=false'
    passwd = H(server_token + b';' + user + b';' + proof)
    return user.hex(), proof.hex(), passwd.hex()


def log_in(username, proof, password):
    if password == H(server_token + b';' + username + b';' + proof):
        if b'is_admin=true' in proof:
            return True
    return False


class Login:
    def __init__(self):
        print(WELCOME)

    def start(self):
        try:
            while True:
                print("\n1- Sign up")
                print("2- Login")
                print("3- Leave")
                c = input("> ")

                if c == '1':
                    usr, prf, pwd = sign_up()
                    print(f"\nAccount created.\nUsername : {usr}\nPassword : {pwd}\nProof : {prf}")

                elif c == '2':
                    user = bytes.fromhex(input("\nUsername : "))
                    passwd = bytes.fromhex(input("Password : "))
                    proof = bytes.fromhex(input("Proof : "))

                    if log_in(user, proof, passwd):
                        N, e, d, pinv = gen_key()
                        print(f"Welcome admin, to continue you need to sign this message : '{message_to_sign}'")
                        print(f"e : {hex(e)}")
                        print(f"d : {hex(d)}")
                        print(f"inverse(p, q) : {hex(pinv)}")

                        sig = input("Enter your signature : ")

                        if verify(sig, e, N):
                            print(f"Long time no see. Here is your flag : {FLAG}")
                        else:
                            sys.exit("Disconnect.")
                    else:
                        sys.exit("Username or password is incorrect.")

                elif c == '3':
                    sys.exit("Goodbye :)")

        except Exception as e:
            print(e)
            sys.exit("System error.")


signal.alarm(60)
if __name__ == "__main__":
    challenge = Login()
    challenge.start()