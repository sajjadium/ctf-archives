from secret import FLAG as FLAAAAAAAAG
from string import ascii_lowercase, digits

M = 10
BLACKLIST = ascii_lowercase + digits + "_()"

for _ in range(3):
    inp = input("> ")
    assert len(inp) < M, "too long"
    assert all(banned not in inp for banned in BLACKLIST), "that's banned"
    exec(inp)
