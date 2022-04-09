import sys
import string
import random
import hashlib

# proof of work
prefix = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
print("Give me a string starting with {} of length {} so its sha256sum ends in ffffff.".format(prefix, len(prefix)+8))
l = input().strip()
if len(l) != len(prefix)+8 or not l.startswith(prefix) or hashlib.sha256(l.encode('ascii')).hexdigest()[-6:] != "ffffff":
    print("Nope.")
    sys.exit(1)
