from Crypto.Util.number import bytes_to_long, long_to_bytes
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from secret import flag, d

assert len(flag) < 256

n = 0xbb7bbd6bb62e0cbbc776f9ceb974eca6f3d30295d31caf456d9bec9b98822de3cb941d3a40a0fba531212f338e7677eb2e3ac05ff28629f248d0bc9f98950ce7e5e637c9764bb7f0b53c2532f3ce47ecbe1205172f8644f28f039cae6f127ccf1137ac88d77605782abe4560ae3473d9fb93886625a6caa7f3a5180836f460c98bbc60df911637fa3f52556fa12a376e3f5f87b5956b705e4e42a30ca38c79e7cd94c9b53a7b4344f2e9de06057da350f3cd9bd84f9af28e137e5190cbe90f046f74ce22f4cd747a1cc9812a1e057b97de39f664ab045700c40c9ce16cf1742d992c99e3537663ede6673f53fbb2f3c28679fb747ab9db9753e692ed353e3551
e = 0x10001
assert pow(2,e*d,n)==2

enc = pow(bytes_to_long(flag),e,n)
print(enc)

k = get_random_bytes(32)
iv = get_random_bytes(16)
cipher = AES.new(k, AES.MODE_CBC, iv)

while 1:
	try:
		i = int(input("Enter message to sign: "))
		assert(0 < i < n)
		print("signed message (encrypted with military-grade aes-256-cbc encryption):")
		print(cipher.encrypt(pad(long_to_bytes(pow(i,d,n)),16)))
	except:
		print("bad input, exiting")
