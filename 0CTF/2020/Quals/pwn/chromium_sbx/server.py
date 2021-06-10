#!/usr/bin/env python3 -u
import hashlib
import os
import random
import string
import sys
import subprocess
import tempfile

MAX_SIZE = 100 * 1024

print("Proof of work is required.")
prefix = "".join([random.choice(string.digits + string.ascii_letters) for i in range(10)])
resource = prefix + "mojo"
bits = 28
cash = input("Enter one result of `hashcash -b {} -m -r {}` : ".format(bits, resource))
r = subprocess.run(["hashcash", "-d", "-c", "-b", str(bits), "-r", resource], input=cash.encode('utf-8'))
if r.returncode != 0:
    print("Nope!")
    exit()

webpage_size = int(input("Enter size: "))
assert webpage_size < MAX_SIZE
print("Give me your webpage: ")
contents = sys.stdin.read(webpage_size)

tmp = tempfile.mkdtemp(dir=os.getenv("WWW"), prefix=bytes.hex(os.urandom(8)))
index_path = os.path.join(tmp, "index.html")
with open(index_path, "w") as f:
    f.write(contents)

sys.stderr.write("New submission at {}\n".format(index_path))

host = "host.docker.internal"
net_args = []
if os.getenv("UNAME") == "Linux":
    net_args.append("--add-host={}:{}".format(host, os.getenv("HOST_IP")))

url = "http://{}:{}/{}/index.html".format(
    host,
    os.getenv("PORT"),
    os.path.basename(tmp)
)
subprocess.run(["docker", "run", "--rm", "--privileged"] + net_args +
               ["mojo", url], stderr=sys.stdout)
