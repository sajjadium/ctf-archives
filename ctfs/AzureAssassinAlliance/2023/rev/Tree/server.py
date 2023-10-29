import os
import uuid
import signal

remote_ip_addr = os.getenv("REMOTE_HOST", "localhost")
identifier = remote_ip_addr + '_' + str(uuid.uuid4())
temp_file = "tmp_{}.cpp".format(identifier)

try:
    signal.alarm(20)
    print('Give me your source code with no header. Input "EOF" to end:', flush=True)
    codes = []
    while True:
        line = input()
        if line == "EOF":
            break
        codes.append(line)
    with open(temp_file, 'w') as f:
        f.writelines(codes)
    res = os.popen(f"./chall {temp_file}").read()
    if(res == "Right!\n"):
        with open("./flag.txt",'r') as f:
            print(f"Here is your flag: {f.read()}", flush=True, end='')
    else:
        print("Try harder.", flush=True)
except:
    print("Hacker!", flush=True)
finally:
    print("Bye~", flush=True)
    os.popen(f"rm {temp_file}")