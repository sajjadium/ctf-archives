#!/usr/bin/env -S python3 -u
import sys
print('length?')
length = int(sys.stdin.buffer.readline())
print('payload?')
payload = sys.stdin.buffer.read(length)
co = compile('','','exec')
eval(co.replace(co_code=payload))
