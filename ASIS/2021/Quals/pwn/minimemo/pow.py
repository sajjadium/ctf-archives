"""
i.e.
sha256("????v0iRhxH4SlrgoUd5Blu0") = b788094e2d021fa16f30c83346f3c80de5afab0840750a49a9254c2a73ed274c

Suffix: v0iRhxH4SlrgoUd5Blu0
Hash: b788094e2d021fa16f30c83346f3c80de5afab0840750a49a9254c2a73ed274c
"""
import itertools
import hashlib
import string

table = string.ascii_letters + string.digits + "._"

suffix = input("Suffix: ")
hashval = input("Hash: ")

for v in itertools.product(table, repeat=4):
    if hashlib.sha256((''.join(v) + suffix).encode()).hexdigest() == hashval:
        print("[+] Prefix = " + ''.join(v))
        break
else:
    print("[-] Solution not found :thinking_face:")
