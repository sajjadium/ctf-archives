#!/usr/local/bin/python3

from os import chdir, system, remove
from shutil import rmtree, unpack_archive
from hashlib import sha256

chdir("/tmp")

ok = {}
if __name__ == "__main__":
    while True:
        rmtree("files", True)
        try: remove("archive.tar.gz")
        except: pass
        match input("[v]alidate or [e]cho? "):
            case "v":
                rawtar = b""
                while (line := input()) != "":
                    rawtar += bytes.fromhex(line)
                with open("archive.tar.gz", "wb") as f:
                    f.write(rawtar)
                unpack_archive("archive.tar.gz", "files", filter="fully_trusted")
                with open("files/message", "rb") as f:
                    if all(c in "abcdefghijklmnopqrstuvwxyzåäö 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ.,".encode() for c in f.readline().strip()):
                        ok[sha256(rawtar).hexdigest()] = ()
                    else:
                        print("🧌")
            case "e":
                rawtar = b""
                while (line := input()) != "":
                    rawtar += bytes.fromhex(line)
                hash = sha256(rawtar).hexdigest()
                if hash not in ok:
                    print("👺")
                    continue
                with open("archive.tar.gz", "wb") as f:
                    f.write(rawtar)
                unpack_archive("archive.tar.gz", "files")
                with open("files/message", "rb") as f:
                    system(b"echo " + f.readline().strip())
