import os
import shutil

base_dir = f"C:\\Users\\balsnctf\\Documents\\Dark Knight\\tmp-{os.urandom(16).hex()}"

def init():
    os.mkdir(base_dir)
    os.chdir(base_dir)

    with open("39671", "w") as f:
        f.write("alice\nalice1025")
    with open("683077", "w") as f:
        f.write("bob\nbob0105a")

def password_manager():
    print("use a short pin code to achieve fast login!!")

    while True:
        pin = input("enter a pin code > ")

        if len(pin) > 100:
            print("too long...")
            continue
        
        if "\\" in pin or "/" in pin or ".." in pin or "*" in pin:
            print("what do you want to do?(¬_¬)")
            continue

        flag = True
        for c in pin.encode("utf8"):
            if c > 0x7e or c < 0x20:
                print("printable chars only!!")
                flag = False
                break
        
        if flag:
            break
    
    while True:
        username = input("enter username > ")

        if len(username) > 100:
            print("too long...")
            continue
        for c in username.encode("utf8"):
            if c > 0x7e or c < 0x20:
                print("printable chars only!!")
                flag = False
                break
        
        if flag:
            break
    
    while True:
        password = input("enter password > ")

        if len(password) > 100:
            print("too long...")
            continue
        for c in password.encode("utf8"):
            if c > 0x7e or c < 0x20:
                print("printable chars only!!")
                flag = False
                break
        
        if flag:
            break

    try:
        with open(pin, "w") as f:
            f.write(username + "\n" + password)
        
        print("saved!!")
    except OSError:
        print("pin is invalid!!")

def safety_guard():
    print("safety guard activated. will delete all unsafe credentials hahaha...")
    delete_file = []
    for pin in os.listdir("."):
        safe = True
        with open(pin, "r") as f:
            data = f.read().split("\n")
            if len(data) != 2:
                safe = False
            elif len(data[0]) == 0 or len(data[1]) == 0:
                safe = False
            elif data[0].isalnum() == False or data[1].isalnum() == False:
                safe = False
            elif data[0] == "admin":
                safe = False

        if safe == False:
            os.remove(pin)
            delete_file.append(pin)
    
    print(f"finished. delete {len(delete_file)} unsafe credentials: {delete_file}")

def fast_login():
    while True:
        pin = input("enter a pin code > ")

        if len(pin) > 100:
            print("too long...")
            continue
        
        if "\\" in pin or "/" in pin or ".." in pin:
            print("what do you want to do?(¬_¬)")
            continue

        flag = True
        for c in pin.encode("utf8"):
            if c > 0x7e or c < 0x20:
                print("printable chars only!!")
                flag = False
                break
        
        if flag:
            break
    
    try:
        with open(pin, "r") as f:
            data = f.read().split("\n")
            if len(data) != 2:
                print("unknown error happened??")
                return None, None
            return data[0], data[1]
    except FileNotFoundError:
        print("this pin code is not registered.")
        return None, None

def normal_login():
    while True:
        username = input("enter username > ")

        if len(username) > 100:
            print("too long...")
        elif username.isalnum() == False:
            print("strange username, huh?")
        elif username == "admin":
            print("no you are definitely not (╬ Ò ‸ Ó)")
        else:
            break
    
    while True:
        password = input("enter password > ")

        if len(password) > 100:
            print("too long...")
            continue
        elif password.isalnum() == False:
            print("strange password, huh?")
        else:
            break
    
    return username, password

def login():
    safety_guard()

    while True:
        print("1. fast login")
        print("2. normal login")
        print("3. exit")
        x = input("enter login type > ")
        if x == "1":
            username, password = fast_login()
        elif x == "2":
            username, password = normal_login()
        elif x == "3":
            print("bye-bye~")
            return
        else:
            print("invalid input.")
            continue

        if username != None and password != None:
            print(f"hello, {username}.")
            if username == "admin":
                while True:
                    x = input("do you want the flag? (y/n): ")
                    if x == "n":
                        print("OK, bye~")
                        return
                    elif x == "y":
                        break
                    else:
                        print("invalid input.")
                while True:
                    x = input("beg me: ")
                    if x == "plz":
                        print("ok, here is your flag: BALSN{flag is here ...}")
                        break
            return

def main():
    init()

    try:
        while True:
            print("1. passord manager")
            print("2. login")
            print("3. exit")
            x = input("what do you want to do? > ")
            if x == "1":
                password_manager()
            elif x == "2":
                login()
            elif x == "3":
                print("bye-bye~")
                break
            else:
                print(f"invalid input: {x}")
    except KeyboardInterrupt:
        print("bye-bye~")
    except:
        print("unexpected error occured.")

    os.chdir("../")
    shutil.rmtree(base_dir)

if __name__ == "__main__":
    main()