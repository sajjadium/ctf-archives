from Crypto.Util.number import bytes_to_long as b2l

secret_1 = Integer(b2l(b'<Redacted 1>'))
secret_2 = Integer(b2l(b'<Redacted 2>'))

assert secret_1.nbits() == 271
assert secret_2.nbits() == 247

real_secret = Mod(secret_1,2^1337 + 1337)/secret_2 + 1337^1337
not_secret_anymore = hex(real_secret^2)
print(not_secret_anymore)

# assert flag  == b"L3AK{" + secret_1 + secret_2 + b"}"
# 0xaf67951fc756caf05e1cb834854880fa6b3919aa390a42a3f2cdcc1943b959192cebea290e4bbe41b517056b95903e9f6ec10d490fdde72cf17a7ab3e65d61fc9c0a750dc20d52626f78c7200744fb9bcc0e7b9f33dd5a83df5d05de7258404b5c56ced4b57e63ab0c7c4761ce76d789734d705e8e137a2000c678c5b90b1df6169499ef39184622d4f83a03985ba8038fdb05aae52d5f2c04f8b8f7a4ac2a54b3d0be67c71752
