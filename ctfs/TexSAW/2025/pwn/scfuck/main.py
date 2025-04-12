#!/usr/bin/python3

import re
from os import chdir
from subprocess import run
from tempfile import TemporaryDirectory

code = input('code? ')
main = input('main? ')

assert re.fullmatch(r'[a-zA-Z_][a-zA-Z0-9_]*', main)
assert len(set(code)) <= 5

gcc = ['gcc', 'a.c', f'-Wl,--defsym=main={main},-T,a.ld']

with TemporaryDirectory() as d:
    chdir(d)
    with open('a.c', 'w') as f:
        f.write(code)
    with open('a.ld', 'w') as f:
        f.write('MEMORY { _ (rwx) : ORIGIN = 0x100000, LENGTH = 0x1000 }')
    assert run(gcc, capture_output=True).returncode == 0
    run(['./a.out'])
