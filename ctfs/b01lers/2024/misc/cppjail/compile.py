#!/bin/env python3
import os
import time

# # local testing stuff
# input_code = []
# while True:
#     try:
#         line = input()
#     except EOFError:
#         break
#     input_code.append(line)
# input_code = ' '.join(input_code)

input_code = input("Input your code: ")
if len(input_code) > 280:
    print("jail must be less than 280 characters !!!")
    exit()

banned_words = [
    "#", "define", "include",
    "//",
    "ifndef", "ifdef",
    "Lock", "Key",
    "class", "struct",
    "*", "int", "char", "short", "long",    
    " "
]

for word in banned_words:
    if word in input_code:
        print("You can't use " + word + " !!!")
        exit()

code = ""
with open("cppjail.cpp", "r") as cjail:
    code = cjail.read()
    code = code.replace("/* you are here */", input_code)

with open("jail.cpp", "w") as cjail_final:
    cjail_final.write(code)

success = os.system("g++ -o jail jail.cpp 2>&1")
if success != 0:
    print("------ Compile errors, skipping")
    exit()

# prevent bruteforce
time.sleep(5)

os.system("./jail 2>&1")
os.system("rm jail")
