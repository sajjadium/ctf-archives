#!/usr/bin/env -S python3 -u
import sys
import re
import os
import signal
import tempfile

ok = re.compile(r'^[a-z0-9_.-]+@[a-z0-9_.-]+\s+//\s+[a-f0-9]{32}$')

print('Send hash list, then end with a blank line')
sys.stdout.flush()
lines = ['import crackstation']

for lino, line in enumerate(sys.stdin.buffer.raw, 1):
    line = line.strip().decode()
    if not line:
        break
    if not ok.match(line):
        print(f'Format error on line {lino}:')
        print(line)
        exit(1)
    lines.append(line)

if len(lines) <= 1:
    print('No tickee, no washee.')
    exit(1)

with tempfile.TemporaryDirectory() as rundir:
    with open(rundir + '/runme.py', 'w') as f:
        for line in lines:
            f.write(line + '\n')
    os.symlink(os.getcwd() + '/crackstation.py', rundir + '/crackstation.py')

    if os.fork() == 0:
        signal.alarm(60)
        argv = ['python3', '-u', rundir + '/runme.py']
        os.execvp(argv[0], argv)
    else:
        os.wait()
