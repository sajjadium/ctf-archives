from os import urandom
from random import getrandbits
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad
import pickle
import time

def generate_number(bits):
    return getrandbits(bits)

class myencryption():
    def __init__(self):
        self.key_counter = 0
        self.encryptions_count = 0
        self.still_single = True
        self.keys = []
        self.username = ""
        self.iv = urandom(16)

    def generate_key(self):
        key = getrandbits(128)
        return long_to_bytes(key)

    def get_recognizer(self):
        self.recognizer = {"id": int(time.time()) * 0xff, "username": self.username, "is_admin": False, "key": self.keys[self.key_counter].hex()}

    def encrypt(self):
        key = self.generate_key()
        self.keys.append(key)
        self.encryptions_count += 1
        self.get_recognizer()
        cipher = AES.new(key, AES.MODE_CBC, iv=self.iv)
        return cipher.encrypt(pad(pickle.dumps(self.recognizer), 16))

    def decrypt(self, data):
        key = self.keys[self.key_counter]
        cipher = AES.new(key, AES.MODE_CBC, iv=self.iv)
        return pickle.loads(cipher.decrypt(data))

header = "=========================================================================================="

def logs(cipher):
    print("Welcome to your inbox !")
    print("---> You have 1 message <---")
    print(f"---> You have encrypted a text {cipher.encryptions_count} times.")
    print(f"---> Unfortunatly you are still single." if cipher.still_single else "You are in a relationship.")
    print(f"---> The current key that was used to encrypt is {cipher.keys[cipher.key_counter].hex()}.")
    print("Thank you for using our service !")

def main():
    cipher = myencryption()
    cipher.username = input("What can I call you ? ")
    print("IV used during this session: ", cipher.iv.hex())
    print(header)
    while True:
        token = cipher.encrypt()
        print("Your new token is : ", token.hex())
        print("Menu:\n1. Logs\n2. Get Flag\n3. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            session_id = bytes.fromhex(input("Would you kindly input your session id: "))
            cipher.iv = session_id[:16]
            decrypted_token = cipher.decrypt(session_id[16:])
            if decrypted_token['is_admin'] == True:
                logs(cipher)
            else:
                print("My apologies, but this is reserved for the admins only.")
        elif choice == 2:
            print("In order to get the flag, you must prove that you are the admin.")
            your_bet = input("What is the key that I'm going to use next ?")
            if your_bet == cipher.generate_key().hex():
                print("Congratulation ! Here is the flag: AKASEC{nn_hh}")
            else:
                print("I am sorry, but you are not the admin.")
                exit()
        elif choice == 3:
            exit()
        else:
            print("Invalid choice. Please try again.")
        cipher.key_counter += 1

if __name__ == "__main__":
    main()
