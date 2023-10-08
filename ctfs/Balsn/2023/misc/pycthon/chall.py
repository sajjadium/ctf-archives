#!/usr/bin/python3 -u
with open('/home/ctf/flag') as f:
    flag = f.read()
payload = input(">>> ")
set_dirty(flag)
sandbox()
eval(payload)