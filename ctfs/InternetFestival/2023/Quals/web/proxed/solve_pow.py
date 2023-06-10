import random
from hashlib import sha256
import sys
import string

if len(sys.argv) != 2:
    print(f'Usage: python {sys.argv[0]} <end-of-hash>')
    exit(1)

pow = sys.argv[1]

while True:
    x = ''.join(random.choices(string.ascii_letters, k=25))

    if( sha256(x.encode()).hexdigest().endswith(pow) ):
        print(x)
        break