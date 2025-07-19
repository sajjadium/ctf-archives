#!/usr/bin/env python3

import base64
from endesive import plain

TO_SIGN = 'just a random hex string: af17a1f2654d3d40f532e314c7347cfaf24af12be4b43c5fc95f9fb98ce74601'
DUCTF_ROOT_CA = open('./root.crt', 'rb').read()

print(f'Sign this! <<{TO_SIGN}>>')
content_info = base64.b64decode(input('Your CMS blob (base64): '))

hashok, signatureok, certok = plain.verify(content_info, TO_SIGN.encode(), [DUCTF_ROOT_CA])

print(f'{hashok = }')
print(f'{signatureok = }')
print(f'{certok = }')

if all([hashok, signatureok, certok]):
    print(open('flag.txt', 'r').read())
