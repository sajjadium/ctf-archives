#!/usr/bin/python3

def blacklist(cmd):
    if cmd.isascii() == False:
        return True
    bad_cmds = ['"',
                "'",
                "print",
                "_",
                ".",
                "import",
                "os",
                "lambda", 
                "system",
                "(",
                ")",
                "getattr",
                "setattr",
                "globals",
                "builtins",
                "input",
                "compile",
                "eval",
                "exec",
                "open",
                "read"]
    for i in bad_cmds:
        if i in cmd:
            return True
    return False
while True:
    inp = input("> ")
    if not blacklist(inp):
        try:
            exec(inp)
        except Exception as e:
            print("snek says: Error!")
            exit(0)
    else:
        print("snek says: Blacklisted!")
        exit(0)
