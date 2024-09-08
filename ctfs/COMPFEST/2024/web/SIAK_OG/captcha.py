import hashlib
import sys
import os


TOTAL_ROUNDS = 92621


def captcha(inp: str):
    s = inp
    for _ in range(TOTAL_ROUNDS):
        inp = hashlib.sha256(s.encode()).hexdigest()
        s = inp[0]
        for i in range(1, len(inp)):
            s += chr(ord(inp[i]) ^ ord(inp[i - 1]) & 0b10101010)

    return hashlib.sha256(s.encode()).hexdigest()


if len(sys.argv) != 2:
    print(f"{os.path.basename(sys.argv[0])} [input]")
    exit()

print(captcha(sys.argv[1]))
