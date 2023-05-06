#!/usr/bin/env python3

from subprocess import run
from sys import stdin, stdout
from struct import pack

command = stdin.buffer.readline().rstrip(b'\n')
result = run(command, shell=True, capture_output=True, timeout=0.5)
header = pack('III', result.returncode, len(result.stdout), len(result.stderr))
message = header + result.stdout + result.stderr
stdout.buffer.write(message)
