with open("flippidy", "rb") as f:
    x = bytearray(f.read())

patch_off = 0x138d
patch = b'\x85\xc0\x74\x02\xc9\xc3'
for i, v in enumerate(patch):
    x[patch_off + i] = v

with open("noflippidy", "wb") as f:
    f.write(x)

