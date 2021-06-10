from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
load('secret.sage')
M = x^127 + x^126 + x^125 + x^124 + x^122 + x^120 + x^118 + x^117 + x^115 + x^108 + x^107 + x^104 + x^103 + x^100 + x^99 + x^98 + x^96 + x^95 + x^94 + x^91 + x^88 + x^85 + x^83 + x^82 + x^81 + x^77 + x^74 + x^72 + x^70 + x^66 + x^65 + x^64 + x^57 + x^56 + x^55 + x^54 + x^50 + x^49 + x^48 + x^46 + x^44 + x^43 + x^37 + x^36 + x^34 + x^33 + x^28 + x^25 + x^22 + x^19 + x^18 + x^17 + x^16 + x^15 + x^14 + x^13 + x^11 + x^10 + x^8 + x^7 + x^4 + x^2 + 1

K.<x> = GF(2^127, 'x', M)
z = x + 1

# for _ in range(n):
#     z = z**69
z = z**ZZ(pow(69, n, z.multiplicative_order()))

print(z)

aes = AES.new(long_to_bytes(n), AES.MODE_ECB)
print(aes.encrypt(flag.encode()).hex())
