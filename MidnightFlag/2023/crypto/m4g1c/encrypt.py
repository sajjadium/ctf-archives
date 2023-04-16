import sys
import os


def get_key(length):
    return os.urandom(length)

def encrypt(filename, key):
    filename_lock = filename + ".lock"
    data = open(filename, "rb").read()
    os.remove(filename)
    locked = open(filename_lock, "wb")
    for idx, i in enumerate(data):
        locked.write((i ^ key[idx % len(key)]).to_bytes(1, "big"))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <file to cipher>")
        exit(0)
    else:
        key = get_key(12)
        encrypt(sys.argv[1], key)
        print("File successfuly encrypted.")
