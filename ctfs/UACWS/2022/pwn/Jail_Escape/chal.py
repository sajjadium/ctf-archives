#!/usr/bin/python3
import os

def main():
    command = input('$ ')
    for k in ['eval', 'exec', 'import', 'open', 'os', 'read', 'system', 'write', 'get']:
        if k in command:
            print("Not allowed")
            return;
    else:
        exec(command)


if __name__ == "__main__":
    print("Flag is at localhost")
    try:
        while True:
            main()
    except Exception as e:
        print(e)


