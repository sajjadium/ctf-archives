Pyjail challenges can only get so difficult they said.

import sys
line = sys.stdin.buffer.readline()
banned = b".()=+-/"
for char in banned:
    if char in line:
        print("Nope")
        break
else:
    print(eval(line, {'globals': {}, '__builtins__': {'getattr': getattr}}))

