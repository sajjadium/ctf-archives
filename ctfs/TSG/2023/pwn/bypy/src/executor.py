from base64 import b64decode
from marshal import loads

NMAX = 10000


def validator(c):
    if len(c.co_names) != 0:
        return False
    if len(c.co_consts) != 0:
        return False
    if len(c.co_cellvars) != 0:
        return False
    if len(c.co_freevars) != 0:
        return False
    if len(c.co_varnames) != 0:
        return False
    return True


def dummy():
    pass


# :)
for key in ["eval", "exec", "__import__", "open"]:
    del __builtins__.__dict__[key]


def main():
    global __builtins__
    print("Give me your source: ")
    src = input()
    if len(src) > NMAX:
        print("too long")
        exit(-1)

    c = b64decode(src)
    code = loads(c)
    if not validator(code):
        print("invalid code")
        exit(-1)

    dummy.__code__ = code

    print(dummy())


main()

