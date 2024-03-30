import ctypes, zlib
from collections import Counter
from secret import FLAG, FLAG2, FLAG3

# See hash_impl.c for implementations of other hash algorithms
c_hash_impl = ctypes.CDLL("./hash_impl.so")
c_hash_wrapper = lambda alg_name: lambda s: ctypes.c_uint(  getattr(c_hash_impl, alg_name)(s) ).value

HASH_ALGS = {
    "hash_bkdr": c_hash_wrapper("hash_bkdr"),
    "hash_djb2": c_hash_wrapper("hash_djb2"),
    "hash_js": c_hash_wrapper("hash_js"),
    "hash_loselose": c_hash_wrapper("hash_loselose"),
    "hash_sdbm": c_hash_wrapper("hash_sdbm"),
    "hash_crc32": zlib.crc32
}

inp = bytes.fromhex(input("Enter string to hash (in hex): "))
assert len(inp) > 1, "short string too boring :("
hash_vals = {name: alg(inp) for name, alg in HASH_ALGS.items()}

for name, hash_val in hash_vals.items():
    print(f"{name}(input) = {hex(hash_val)}")

if max(Counter(hash_vals.values()).values()) == 3:
    print(f"Collision found! flag: {FLAG}")
elif max(Counter(hash_vals.values()).values()) == 4:
    print(f"More collision found! flag: {FLAG2}")
elif max(Counter(hash_vals.values()).values()) > 4:
    print(f"Woah. flag: {FLAG3}")
else:
    print("No collision - try again!")
