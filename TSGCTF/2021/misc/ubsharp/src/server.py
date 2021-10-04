from secrets import SystemRandom
from string import Template
from hashlib import sha256
from base64 import b64decode,b64encode
import signal
import sys
import subprocess as sp
import os
randgen = SystemRandom()

TIMEOUT=60
if "SERVER_TIMEOUT" in os.environ:
    TIMEOUT = int(os.environ["SERVER_TIMEOUT"])
def handler(x, y):
    sys.exit(1)
signal.signal(signal.SIGALRM, handler)
signal.alarm(TIMEOUT)

PROGRAM_MAX_LEN = 0x50000

parentheses = [
    ["(", ")"],
    ["{", "}"],
    ["[", "]"],
]
blacklist_words = ['`', '@', '$', '\\', '#', '"', "'", "//", "/*", "using", "unsafe",
                   "Reflection", "IO", "File", "Console", "Net",
                   "Accessibility", "Microsoft", "System", "UI"]
hello_output = """read until 'END\\n'"""

def sanitizer(input_str):
    for word in blacklist_words:
        if word in input_str:
            return False
    stack = []
    for c in input_str:
        for p in parentheses:
            if p[0] == c:
                stack.append(p[1])
                break
            if p[1] == c:
                if len(stack) > 0 and stack[-1] == p[1]:
                    stack.pop()
                else:
                    return False
    if len(stack)>0:
        return False

    return True

def save_ans(ans):
    with open('/userans/'+sha256(ans.encode('ascii')).hexdigest()+'.cs','w') as f:
        f.write(ans)

if __name__ == '__main__':
    template_txt = ""
    user_input = ""
    password = ""
    session = ""

    for i in range(60):
        password += chr(randgen.randrange(ord('a'), ord('z')+1))

    for i in range(60):
        session += chr(randgen.randrange(ord('a'), ord('z')+1))
    
    template_path = "./template.cs"
    with open(template_path, 'r') as f:
        template_txt = f.read()
    print(hello_output)
    tmp = ""
    while tmp != "END":
        user_input += tmp+'\n'
        tmp = input()
        if len(user_input) > PROGRAM_MAX_LEN:
            print("too long!!")
            sys.exit()
    if not sanitizer(user_input):
        print("Evil input")
        sys.exit()
    s = Template(template_txt)
    user_output = (s.substitute(user_input=user_input, password=password))
    print("following program is run")
    print(user_output)
    res = None
    try:
        res = sp.run(['./copy_proj.sh', session], capture_output=True, check=True)
    except sp.CalledProcessError:
        print("Copy failed")
        sys.exit()
    with open("/tmp/"+session+"/Program.cs", 'w') as f:
        f.write(user_output)
    try:
        res = sp.run(['./build_proj.sh', session], capture_output=True, check=True)
    except sp.CalledProcessError:
        print("Build error")
        if "DEBUG" not in os.environ:
            sp.run(['./rm_proj.sh', session], capture_output=True)
        sys.exit()
    try:
        res = sp.run(['./run_proj.sh', session], capture_output=True)
        if res.stdout == (password+'\n').encode('ascii'):
            import os
            print("Congratulations!",os.environ['FLAG'])
            save_ans(user_input)
        else:
            print("Failed...")
            if "DEBUG" in os.environ:
                print(res.stdout.decode('ascii'),res.stderr.decode('ascii'))
            sp.run(['./rm_proj.sh', session], capture_output=True)
    except sp.CalledProcessError:
        print("Runtime error")
    sp.run(['./rm_proj.sh', session], capture_output=True)
    sys.exit()
