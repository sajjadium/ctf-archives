from KeyRecoveryScheme import KeyRecoveryScheme
from questions import questions
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import bcrypt
import json
import base64
from os import path
from sys import exit
from client_unlock import get_db_entry

def main():
    print("Welcome to the password recovery wizard!")
    username = input("Enter the username you want to save the password for: ")
    entry = get_db_entry(username)
    if (entry != None):
        print("There already exists an entry in the password database with the same username.")
        answer = input("Do you wish to proceed? The old entry will be replaced (Y/N): ")
        if (answer.lower() != "y"):
            print("Aborting.")
            exit()
    password = input("Enter the password you want to recover later on: ") # the password is the flag
    print("Next, you will have to answer a series of 12 questions. The answers to these questions will be used to secure your password.")
    print("We will begin the questions now.")
    print()

    answers = []
    for i in range(len(questions)):
        ans = str(input(questions[i] + " "))
        answers.append((i + 1, ans)) # (i + 1) because the question # is 1-indexed

    krs = KeyRecoveryScheme(10, 12)
    (aes_key, lock) = krs.Lock(answers)
    aes_cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_password = aes_cipher.encrypt(pad(password.encode(), 16))

    password_bcrypt = bcrypt(password, 12)

    if (not path.isfile("data.json")):
        with open("data.json", "w") as json_file:
            json_file.write("[]")

    with open("data.json") as json_file:
        password_database = json.load(json_file)

    new_entry = {
        "username": username,
        "encrypted_password": base64.b64encode(encrypted_password).decode(),
        "lock": lock.decode(),
        "password_bcrypt": password_bcrypt.decode()
    }

    if (entry == None):
        password_database.append(new_entry)
    else:
        for i in range(len(password_database)):
            if (password_database[i]["username"] == username):
                password_database[i] = new_entry
                break

    with open("data.json", "w") as json_file:
        json.dump(password_database, json_file, indent=4)

    print("\nSaved the following parameters to data.json:")
    print("--------------------------------------------------------------")
    print(f"username = {username}")
    print(f"encrypted_password = {base64.b64encode(encrypted_password).decode()}")
    print(f"lock = {lock.decode()}")
    print(f"password_bcrypt = {password_bcrypt.decode()}")
    print("--------------------------------------------------------------")

if __name__ == "__main__":
    main()