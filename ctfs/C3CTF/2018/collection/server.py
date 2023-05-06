import os
import tempfile
import os
import string
import random

def randstr():
    return ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(10))


flag = open("flag", "r")


prefix = """
from sys import modules
del modules['os']
import Collection
keys = list(__builtins__.__dict__.keys())
for k in keys:
    if k != 'id' and k != 'hex' and k != 'print' and k != 'range':
        del __builtins__.__dict__[k]

"""


size_max = 20000

print("enter your code, enter the string END_OF_PWN on a single line to finish")


code = prefix
new = ""
finished = False

while size_max > len(code):
    new = raw_input("code> ")
    if new == "END_OF_PWN":
        finished = True
        break
    code += new + "\n"

if not finished:
    print("max length exceeded")
    sys.exit(42)


file_name = "/tmp/%s" % randstr()
with open(file_name, "w+") as f:
    f.write(code.encode())


os.dup2(flag.fileno(), 1023)
flag.close()

cmd = "python3.6 -u %s" % file_name
os.system(cmd)
