#!/usr/bin/env python3

def server():
    message = """
    You are in jail. Can you escape?
"""
    print(message)
    while True:
        try:
            data = input("> ")
            safe = True
            for char in data:
                if not (ord(char)>=33 and ord(char)<=126):
                    safe = False
            with open("blacklist.txt","r") as f:
                badwords = f.readlines()
            for badword in badwords:
                if badword in data or data in badword:
                    safe = False
            if safe:
                print(exec(data))
            else:
                print("You used a bad word!")
        except Exception as e:
            print("Something went wrong.")
            print(e)
            exit()

if __name__ == "__main__":
    server()