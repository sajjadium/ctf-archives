from ecdsa import SigningKey
import secrets
sk = SigningKey.generate()
pk = sk.verifying_key

message = secrets.token_bytes(16)
print("Hello,", message.hex())
sig = sk.sign(message)
print(sig.hex())

print("Here's my public key")
print(pk.to_der().hex())

print("What was my private key again? (send me DER-encoded hex bytes)")
der = bytes.fromhex(input(""))

sk2 = SigningKey.from_der(der)
vk2 = sk2.verifying_key

assert sk2.privkey.secret_multiplier * sk2.curve.generator == vk2.pubkey.point
assert vk2.verify(sig, message)

with open("flag") as f:
    flag = f.read()
    print(flag, sk2.sign(flag.encode()))
