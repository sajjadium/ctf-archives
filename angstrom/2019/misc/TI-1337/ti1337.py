#!/usr/bin/env python3
del __builtins__.__import__
__builtins__.print("Welcome to the TI-1337! You can use any math operation and variables with a-z.")
_c = ""
_l = __builtins__.input("> ")
while _l != "":
    # division -> floor division
    _l = _l.replace("/", "//")
    _c += _l+"\n"
    _l = __builtins__.input("> ")
_v = {}
_v = __builtins__.set(__builtins__.dir())
__builtins__.exec(_c)
for _var in __builtins__.set(__builtins__.dir())-_v:
    __builtins__.print(_var, "=", __builtins__.vars()[_var])
