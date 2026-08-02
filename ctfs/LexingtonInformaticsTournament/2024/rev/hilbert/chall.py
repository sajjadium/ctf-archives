from subprocess import run, DEVNULL

whitelist = '驗故若非>Ⅰ,Ⅱ;Ⅲ<𝑝'
code = input()

if any(c not in whitelist for c in code):
    print('banned character')
    exit()

with open('main.cpp', 'w') as f:
    f.write('#include "hi.h"\n')
    f.write(code)

if run(['g++', 'main.cpp', '-o', 'main'], stdout=DEVNULL, stderr=DEVNULL).returncode != 0:
    print('failed to compile')
    exit()

print(run(['./main'], capture_output=True, text=True).stdout, end='')
