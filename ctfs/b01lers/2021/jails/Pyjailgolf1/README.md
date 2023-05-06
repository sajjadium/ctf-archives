You have 10 characters to get the flag. Have fun!

line = input('>>> ')

flag="[REDACTED]"

if len(line) > 10:
    raise Exception()

try:
    eval(line)
except:
    pass

