#!/usr/bin/python3

from os import chdir
from subprocess import run
from tempfile import TemporaryDirectory

code = input('code? ')

assert len(set(code)) <= 12

with TemporaryDirectory() as d:
    chdir(d)
    with open('a.c', 'w') as f:
        f.write(code)
    assert run(['gcc', 'a.c'], capture_output=True).returncode == 0
    run(['./a.out'])
