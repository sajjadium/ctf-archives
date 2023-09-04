import sys
import hashlib

if len(sys.argv) != 2:
    print("python3 flag.py <input>")
    exit()

print("WACON2023{" + hashlib.sha256(sys.argv[1].encode()).hexdigest() + "}")

