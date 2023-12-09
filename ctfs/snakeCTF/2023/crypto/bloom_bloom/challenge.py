from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import random
import signal
import mmh3

TIMEOUT = 300

assert("FLAG" in os.environ)
FLAG = os.environ["FLAG"]
assert(FLAG.startswith("CTF{"))
assert(FLAG.endswith("}"))



alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
users = 0b0
hash_functions_count = 5
size = 256 # number of bits
logged_in = False

key = os.urandom(16)
iv = os.urandom(16)

def check_user(username):
    global users
    cipher = AES.new(key, AES.MODE_ECB)
    enc_username = cipher.encrypt(pad(username.encode(), AES.block_size))
    
    for i in range(hash_functions_count):
        digest = mmh3.hash(enc_username, i) % size
        if users & (0x1 << digest) == 0:
            return False
    
    return True

def add_user(username):
    global users

    cipher = AES.new(key, AES.MODE_ECB)
    enc_username = cipher.encrypt(pad(username.encode(), AES.block_size))
    for i in range(hash_functions_count):
        digest = mmh3.hash(enc_username, i) % size
        users = users | (0x1 << digest)
    

def login():
    global logged_in
    logged_in = True

def logout():
    global logged_in
    logged_in = False

def is_valid(username):
    global alphabet
    
    if len(username) > 128:
        return False

    for c in username:
        if c not in alphabet:
            return False

    return True


def main():
    print("__ Welcome to the super secure Database __")

    while True:

        print("""
            1) Login 
            2) Login as Administrator
            3) Register
            4) Logout
            5) Exit
            """)

        choice = input("> ")

        if choice == "1":
            if logged_in:
                print("You are already logged in.")
                continue

            username = input("Username: ")

            if not is_valid(username):
                print("Invalid username!")
                continue

            if username == "Administrator":
                print("Forbidden!")
                continue

            if check_user(username):
                print(f"Login successfull! Welcome back {username}")
                login()
            else:
                print(f"The user {username} does not exist")

        elif choice == "2": 
            if logged_in:
                print("You are already logged in with a different username")
                continue

            if check_user("Administrator"):
                print(f"Welcome back Administrator")
                print(f"Here is your flag: {FLAG}")
            else:
                print("Administrator is not a valid user in the database")

        elif choice == "3": 
            username = input("Username: ")
            if not is_valid(username):
                print("Invalid username!")
                continue

            if username == "Administrator":
                print("Forbidden!")
                continue

            if check_user(username):
                print(f"Such username already exists!")
                continue

            add_user(username)
            print(f"Good job {username}! You are now able to Login")

        elif choice == "4": 
            if logged_in:
                logout()
                print("GoodBye!")
            else:
                print("You are not logged in!")
                
        elif choice == "5": 
            break




if __name__ == "__main__":
    signal.alarm(TIMEOUT)
    main()