#!/usr/local/bin/python -u
import hashlib
import os

with open("flag.txt") as f:
    FLAG = f.read()

QUERIED = set()
KEY = os.urandom(16)

print("Introducing Neil-MAC (NMAC), the future of hash-based message")
print("authentication codes!")
print()
print("No longer susceptible to those pesky length extension attacks!")
print()

def nmac(message):
    return hashlib.md5(message + KEY).hexdigest()

def query():
    print("What message would you like to query a tag for?")
    print("Enter message hex-encoded:")
    hex_message = input()
    message = bytes.fromhex(hex_message)
    QUERIED.add(message)
    print("Tag:", nmac(message))

def challenge():
    print("Challenge time!")
    print("Enter message hex-encoded:")
    hex_message = input()
    tag = input("Tag: ")
    message = bytes.fromhex(hex_message)
    if message in QUERIED:
        print("You already queried that message!")
    elif nmac(message) == tag:
        print("Nice job!")
        print("Flag:", FLAG)

while True:
    print("What do you want to do?")
    print("1) Query a message")
    print("2) Challenge")
    match input():
        case "1":
            query()
        case "2":
            challenge()
            break
        case _:
            print("???")
