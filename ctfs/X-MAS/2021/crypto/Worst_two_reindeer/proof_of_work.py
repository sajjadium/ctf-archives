import os
import string
import sys
import functools
from binascii import unhexlify
from hashlib import sha256


def proof_of_work(nibble_count: int) -> bool:
    rand_str = os.urandom(10)
    rand_hash = sha256(rand_str).hexdigest()

    print(f"Provide a hex string X such that sha256(unhexlify(X))[-{nibble_count}:] = {rand_hash[-nibble_count:]}\n")
    sys.stdout.flush()

    user_input = input()
    is_hex = functools.reduce(lambda x, y: x and y, map(lambda x: x in string.hexdigits, user_input))

    if is_hex and sha256(unhexlify(user_input)).hexdigest()[-nibble_count:] == rand_hash[-nibble_count:]:
        print("Good, you can continue!")
        sys.stdout.flush()
        return True
    else:
        print("Oops, your string didn\'t respect the criterion.")
        sys.stdout.flush()
        return False