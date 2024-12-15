# unsafe (example of what not to do)
def unsafe_eval():
    inp = input("> ")
    eval(inp)

# 100% safe
BLACKLIST = ["builtins", "import", "=", "flag", ';', "print", "_", "open", "exec", "eval", "help", "br"]
def safe_eval():
    inp = input("> ")
    if any(banned in inp for banned in BLACKLIST) or any(ord(c) >= 128 for c in inp):
        print('bye')
        exit()
    eval(inp)

safe_eval()