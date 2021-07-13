#!/usr/bin/env python3
import random
from secret import flag

key = random.randint(10**7, 10**8)

out = b""

for c in flag:
    out += bytes([c ^ (key&0xff)])
    key = int("{:016d}".format(key**2)[4:12])
    
print(f"{out.hex()}")

# Output:
# e649fd7458fb36acb341346324635da87427d8d25f5c8b7665b921052727bf730f1c0273d00c23217873