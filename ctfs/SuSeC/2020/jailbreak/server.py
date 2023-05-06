#!/usr/bin/env python
import ctypes

# We use external library because built-in functions are deleted
# and default 're' will no longer work.
#  - https://github.com/kokke/tiny-regex-c
libregex = ctypes.CDLL('./libregex.so')
match = libregex.re_match
match.restype = ctypes.c_int
match.argtypes = [ctypes.c_char_p, ctypes.c_char_p]

# code blacklist
blacklist = [
    'eval', 'exec', 'setattr', 'system', 'open'
]
# built-in whitelist
whitelist = [
    'print', 'eval', 'input', 'int', 'str', 'isinstance', 'setattr',
    '__build_class__', 'Exception', 'KeyError'
]

def check_code(code):
    if match(b'[-a-zA-Z0-9,\\.\\(\\)]+$', code.encode()) != 0:
        raise Exception("Invalid code")
    for word in blacklist:
        if word in code:
            raise Exception("'" + word + "' is banned")

def run_code():
    code = input('code: ')
    check_code(code)
    eval(code)

if __name__ == '__main__':
    for name in dir(__builtins__):
        if name not in whitelist:
            del __builtins__.__dict__[name]
    try:
        run_code()
        print("[+] Done!")
    except Exception as e:
        print("[-] " + str(e))
