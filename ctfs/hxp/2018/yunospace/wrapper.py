#!/usr/bin/python3 -u

import sys, os, base64

FLAG = "hxp{find_the_flag_on_the_server_here}"

print(" y-u-no-sp                ")
print("XXXXXXXXx.a               ")
print("OOOOOOOOO|                ")
print("OOOOOOOOO| c              ")
print("OOOOOOOOO|                ")
print("OOOOOOOOO|                ")
print("OOOOOOOOO| e              ")
print("~~~~~~~|\~~~~~~~\o/~~~~~~~")
print("   }=:___'>             \n")

print("> Welcome. Which byte should we prepare for you today?")

try:
    n = int(sys.stdin.readline())
except:
    print("> I did not get what you mean, sorry.")
    sys.exit(-1)

if n >= len(FLAG):
    print("> That's beyond my capabilities. Goodbye.")
    sys.exit(-1)

print("> Ok. Now your shellcode, please.")

os.execve("./yunospace", ["./yunospace", FLAG[n]], dict())
