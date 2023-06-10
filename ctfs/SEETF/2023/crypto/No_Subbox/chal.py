from aes import encrypt_block, Element, N_BYTES
from secrets import randbelow

key = bytes([randbelow(Element.sz) for _ in range(N_BYTES)])
pt = bytes([randbelow(Element.sz) for _ in range(N_BYTES)])
ct = encrypt_block(key, pt)

print(f"pt = {pt.hex()}")
print(f"ct = {ct.hex()}")
print("flag = SEE{%s}"%key.hex())

### Truncated printed output below

# pt = f085c01fefa2af35326467f6facfcf50
# ct = a016124ed2b337a845ca03be0dd014cd