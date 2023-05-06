Now you have 9 characters to get the flag. Good luck!

line = input('>>> ')

flag="[REDACTED]"

if len(line) > 9:
    raise Exception()

try:
    eval(line)
except:
    pass

