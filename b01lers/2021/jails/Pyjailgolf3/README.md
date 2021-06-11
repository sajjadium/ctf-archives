line = input('>>> ')
# Some code here to remove that function that you used to solve pyjailgolf 2 from builtins
# The only reason it is censored is to not spoil pyjailgolf 2.
builtins = [REDACTED]

flag="[REDACTED]"

if len(line) > 10:
    raise Exception()

try:
    eval(line, {'__builtins__': builtins}, locals())
except:
    pass
