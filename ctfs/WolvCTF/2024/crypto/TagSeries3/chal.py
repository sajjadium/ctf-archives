import sys
import os
from hashlib import sha1

MESSAGE = b"GET FILE: "
SECRET = os.urandom(1200)


def main():
    _sha1 = sha1()
    _sha1.update(SECRET)
    _sha1.update(MESSAGE)
    sys.stdout.write(_sha1.hexdigest() + '\n')
    sys.stdout.flush()
    _sha1 = sha1()
    command = sys.stdin.buffer.readline().strip()
    hash = sys.stdin.buffer.readline().strip()
    _sha1.update(SECRET)
    _sha1.update(command)
    if command.startswith(MESSAGE) and b"flag.txt" in command:
        if _sha1.hexdigest() == hash.decode():
            with open("flag.txt", "rb") as f:
                sys.stdout.buffer.write(f.read())


if __name__ == "__main__":
    main()
