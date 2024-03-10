#!/usr/bin/env python3

flag = 'wxmctf{REDACTED}'
encoded = ''

for c in flag:
    encoded += ''.join(map(
        lambda x: format(int(x), 'b').zfill(4),
        str(ord(c)).zfill(3)
    ))

with open('output.txt', 'w') as output:
    output.write(encoded)
