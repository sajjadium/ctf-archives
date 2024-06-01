import os
import hashlib
from datetime import datetime
from admin import admin

def sort_messages(messages):
    try:
        messages.sort(key=lambda x: datetime.strptime(x[1][:19], "%Y-%m-%d %H:%M:%S"))
    except:
        pass
    return messages

def create_account():
    name = input("Enter your username: ")
    names = os.listdir("./log")
    while name in names or name == "":
        name = input("This username is either already used or empty! Enter another one: ")
    passwd = input("Enter a password: ")
    log = open(f"./log/{name}", 'w')
    log.write(f"Password : {hashlib.md5(passwd.encode()).hexdigest()}\n")
    print("\nAccount was successfully created!")
    log.close()

def connect():
    name = input("Username: ")
    names = os.listdir("./log")
    while not(name in names):
        name = input("This user does not exists! Username: ")
    log = open(f"./log/{name}", 'r+')
    hash_pass = log.readline().split(" ")[-1][:-1]
    return (hashlib.md5(input("Password: ").encode()).hexdigest() == hash_pass, name)

def get_all_messages():
    names = os.listdir("./log")
    messages = []
    for name in names:
        with (open(f"./log/{name}", 'r')) as log:
            for line in log.readlines()[1:]:
                messages.append((name, line))
    return sort_messages(messages)

def send_message(name):
    message = input("Entre your message: ")
    with (open(f"./log/{name}", 'a')) as log:
        log.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}\n")
    print("\nYour message has been sent!")

connected = False

print("Hey, welcom to j0j0 Chat! Feel free to chat with everyone here :)")

while True:
    if not connected:
        option = input("\nChoose an option:\n1) Create an account\n2) Login\n3) Leave\n")
        match option:
            case "1":
                create_account()
            case "2":
                connected, name = connect()
                if not(connected):
                    print("Incorrect password!")
            case "3":
                print("Bye! Come back whenever you want!")
                exit()
    else:
        option = input("\nChoose an option:\n1) See messages\n2) Send a message\n3) Logout\n")
        match option:
            case "1":
                print()
                messages = get_all_messages()
                for message in messages:
                    print(f"{message[0]} : {message[1][20:]}", end="")
            case "2":
                send_message(name)
            case "3":
                print("\nYou successfully logged out!")
                connected = False
            case "admin":
                if name == "admin":
                    admin()