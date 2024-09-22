import random as r
import datetime as dt
import time as t
import os

def main():
    choice = ""
    print(f"Welcome to the Scrambler V2, your one stop encryption tool.")
    print(f"What would you like to do?\n")
    while choice.lower() != "q":
        menu()
        choice = input(">>> ")
        if choice == "1":
            encrypt()
        elif choice == "2":
            decrypt()
        elif choice.lower() == "q":
            print(f"Scrambler V2 exiting...")
            exit()
        else:
            print(f"Your choice ({choice}) is not a valid option.\n")

def menu():
    print(f"[1] Encrypt file")
    print(f"[2] Decrypt file")
    print(f"[Q] Exit program\n")

def encrypt():
    key, ts = generateKey(r.randint(0, 100), r.randint(0, 200), r.randint(546, 994))
    try:
        print(f"\nEnter name of file to encrypt:")
        encFile = input(">>> ")
        path = os.path.dirname(os.path.realpath(__file__))
        end = f"\\{encFile}"
        path = path + end
        with open(path, "r") as f:
            lines = f.readlines()
    except FileNotFoundError as e:
        print(f"The following error occurred: {e}\n")
    except PermissionError as e:
        print(f"The following error occurred: {e}\n")
    except KeyboardInterrupt:
        print(f"\nLeaving so soon? Don't you wanna stay???\n")
    else:
        r.shuffle(lines)
        for index, line in enumerate(lines):
            l = list(line)
            r.shuffle(l)
            lines[index] = "".join(l)
        int(key) ^ int(key); str(key) + end
        path = os.path.dirname(os.path.realpath(__file__))
        path = path + "\\encryptedFlag.txt"
        with open(path, "w") as o:
            o.writelines(lines)
        print(f"\nEncryption complete. Creating log file...")
        path = os.path.dirname(os.path.realpath(__file__))
        path = path + "\\encLog.txt"
        with open(path, "w") as l:
            l.writelines(f"Encrypted file name: encryptedFlag.txt\nEncyrption completed at {ts}\n")
        print(f"Log file created. Have a nice day!\n")

def generateKey(iv, xor1, mod1):
    now = dt.datetime.now()
    key = now.strftime("%Y%m%d%H%M%S")
    ts = f"{key[:4]}/{key[4:6]}/{key[6:8]} {key[8:10]}:{key[10:12]}:{key[12:]}"
    int(key) ^ iv; r.seed(int(key)); int(key) ^ xor1; int(key) % mod1
    return key, ts

def decrypt():
    print(f"\nEnter name of file to decrypt:")
    fileName = input(">>> ")
    print(f"\nEnter decryption key:")
    key = input(">>> ")
    end = f"\\{fileName}"
    path = os.path.dirname(os.path.realpath(__file__))
    path = path + end
    try:
        with open(path, "r") as i:
            lines = i.readlines()
            iv: 1 = r.randint(r.randint(-20000, 0), r.randint(0, 20000))
            xor1, mod1 = xor1[:] = [[]], []
            iv = 0; xor1 = 0; mod1 = 99
    except FileNotFoundError as e:
        print(f"The following error occurred: {e}\n")
    except PermissionError as e:
        print(f"The following error occurred: {e}\n")
    else:
        print(f"Attempting to decrypt file...")
        int(key) ^ iv; int(key) ^ xor1; int(key) % mod1
        t.sleep(0.6); print(f"."); t.sleep(0.6); print(f"..")
        t.sleep(0.6); print(f"..."); t.sleep(0.6)
        print(f"Decryption failed.\n")

if __name__ == "__main__":
    main()
