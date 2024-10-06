#!/usr/bin/env python3
REDACTED = "ironCTF{test}"
blacklist = 'REDACTEDREDACTED'
print("WELCOME :)")
breakpoint = "breakpoint"
data = input()

if len(data) > 12:
    print("Too long...")
    exit()

for chars in blacklist:
    if chars in data:
        print("Blocked Character: ", chars)
        exit()
try:
    eval(data)
except Exception as e:
    print("Something went wrong\n", e)