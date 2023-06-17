import subprocess
import tempfile 
import base64
import os

code = input('Enter Your base64 > ')

try:
    code = base64.b64decode(code)
except:
    print('base64 error')
    exit(1)

if b'#' in code:
    print('error')
    exit(1)

_, filename = tempfile.mkstemp(prefix='ctf-')

f = open(filename, 'wb')
f.write(code)
f.close()

p = subprocess.Popen(['./cst', filename], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait(timeout=3)

print('======= stdout =======')
print(p.stdout.read().decode())
print('======= stderr =======')
print(p.stderr.read().decode())

# os.unlink(filename)
