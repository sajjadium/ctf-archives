from Crypto.Cipher import AES
from secret import key, FLAG

p = 4170887899225220949299992515778389605737976266979828742347
ct = bytes.fromhex("ae7d2e82a804a5a2dcbc5d5622c94b3e14f8c5a752a51326e42cda6d8efa4696")

def crack_safe(key):
    return pow(7, int.from_bytes(key, 'big'), p) == 0x49545b7d5204bd639e299bc265ca987fb4b949c461b33759

assert crack_safe(key) and AES.new(key,AES.MODE_ECB).decrypt(ct) == FLAG
