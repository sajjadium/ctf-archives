from hashlib import sha256
from Crypto.Cipher import AES

x = int(input('Enter an 8-digit multiplicand: '))
y = int(input('Enter a 7-digit multiplier: '))
assert 1e6 <= y < 1e7 <= x < 1e8, "Incorrect lengths"
assert x * y != 3_81_40_42_24_40_28_42, "Insufficient ntr-opy"

def dream_multiply(x, y):
    x, y = str(x), str(y)
    assert len(x) == len(y) + 1
    digits = x[0]
    for a, b in zip(x[1:], y):
        digits += str(int(a) * int(b))
    return int(digits)
assert dream_multiply(x, y) == x * y, "More like a nightmare"

ct = '75bd1089b2248540e3406aa014dc2b5add4fb83ffdc54d09beb878bbb0d42717e9cc6114311767dd9f3b8b070b359a1ac2eb695cd31f435680ea885e85690f89'
print(AES.new(sha256(str((x, y)).encode()).digest(), AES.MODE_ECB).decrypt(bytes.fromhex(ct)).decode())