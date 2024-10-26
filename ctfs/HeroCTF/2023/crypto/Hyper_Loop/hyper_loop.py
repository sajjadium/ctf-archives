from os import urandom


flag = bytearray(b"Hero{????????????}")
assert len(flag) == 18

for _ in range(32):
    for i, c in enumerate(urandom(6) * 3):
        flag[i] = flag[i] ^ c

print(f"{flag = }")


"""
$ python3 hyper_loop.py 
flag = bytearray(b'\x05p\x07MS\xfd4eFPw\xf9}%\x05\x03\x19\xe8')
"""
