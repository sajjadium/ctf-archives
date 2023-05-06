from KeyRecoveryScheme import KeyRecoveryScheme
from questions import questions
from Crypto.Util.Padding import unpad
from Crypto.Protocol.KDF import bcrypt_check
from Crypto.Cipher import AES
import json
from sys import exit
import base64

def get_db_entry(username):
    with open("data.json") as json_file:
        password_database = json.load(json_file)
    for entry in password_database:
        if (entry["username"] == username):
            return entry
    return None # if no match is found

def main():
    print("Welcome to the password recovery wizard!")
    username = input("Enter the username whose password you want to recover: ")
    entry = get_db_entry(username)

    if (entry == None):
        print("Could not find username in database.")
        exit()

    encrypted_password = base64.b64decode(entry["encrypted_password"])
    lock = entry["lock"].encode()
    password_bcrypt = entry["password_bcrypt"].encode()

    print("To recover your password, you will have to answer a series of questions.")
    print("You only have to answer 10 of the 12 questions.")
    print("To skip a question, simply hit Return without entering any input.")
    print("We will begin the questions now.")
    print()

    answers = []
    for i in range(len(questions)):
        ans = str(input(questions[i] + " "))
        if (ans == ""):
            continue
        answers.append((i + 1, ans)) # (i + 1) because the question # is 1-indexed

    try:
        krs = KeyRecoveryScheme(10, 12)
        aes_key = krs.Unlock(answers, lock)
        aes_cipher = AES.new(aes_key, AES.MODE_ECB)
        password = unpad(aes_cipher.decrypt(encrypted_password), 16)
        bcrypt_check(password, password_bcrypt)
        print("Password recovery successful! Here is your password:")
        print(password.decode())
    except ValueError:
        print("There was an error in unpadding.")
        print("Password recovery failed.")
    except AssertionError:
        print(f"You need to answer at least 10 security questions to recover the password, but you only gave {len(answers)} answers.")
        print("Password recovery failed.")

if __name__ == "__main__":
    main()