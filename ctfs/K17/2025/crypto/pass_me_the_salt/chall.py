from hashlib import sha1
import os

logins = {}
salts = {}

def create_account(login, pwd):
    if login in logins.keys():
        return False
    
    salt = os.urandom(16)
    salted_pwd = salt + (pwd).encode()
    passw = sha1(salted_pwd).hexdigest()
    
    logins[login] = passw
    salts[login] = salt

    return True

def check_login(login, pwd):
    if login not in logins:
        return False

    salt = salts[login]
    salted_pwd = salt + bytes.fromhex(pwd)

    passw = sha1(salted_pwd).hexdigest()
    return passw == logins[login]

def change_password(login, new_pass):
    if login not in logins:
        return
    
    print(f"Current password: {logins[login]}")

    logins[login] = new_pass

if __name__ == "__main__":
    create_account("admin", "admin".encode().hex())

    while True:
        option = input("1. Create Account\n2. Login\n3. Change Password\n(1, 2, 3)> ")
        if option == "1":
            login = input("Login: ")
            pwd = input("Password: ")
            if create_account(login, pwd.encode().hex()):
                print("Account created!")
            else:
                print("Could not create account.")
        elif option == "2":
            login = input("Login: ")
            pwd = input("Password: ")

            if not check_login(login, pwd):
                print("Invalid login or password.")
                continue

            if login == "admin":
                if pwd != "admin".encode().hex():
                    print(f"Congratulations! Here is your flag: {os.getenv("FLAG")}")
                else:
                    print("Your flag is in another castle...")
            else:
                print(f"Login successful as {login}!")
        elif option == "3":
            login = input("Login: ")
            new_pass = input("New password: ")

            change_password(login, new_pass)
            print("Password changed!")
        else:
            print("Invalid option.")
