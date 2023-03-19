#!/usr/bin/python3

modulus = 1 << 258

def Z2kDH_init(private_exponent):
	"""
	Computes the public result by taking the generator 5 to the private exponent, then removing the last 2 bits
	private_exponent must be a positive integer less than 2^256
	"""
	return pow(5, private_exponent, modulus) // 4

def Z2kDH_exchange(public_result, private_exponent):
	"""
	Computes the shared secret by taking the sender's public result to the receiver's private exponent, then removing the last 2 bits
	public_result must be a non-negative integer less than 2^256
	private_exponent must be a positive integer less than 2^256
	"""
	return pow(public_result * 4 + 1, private_exponent, modulus) // 4

alice_private_exponent = int(open('alice_private_exponent.txt').read(), 16)
bob_private_exponent = int(open('bob_private_exponent.txt').read(), 16)

alice_public_result = Z2kDH_init(alice_private_exponent)
bob_public_result = Z2kDH_init(bob_private_exponent)

# These are sent over the public channel:
print(f'{alice_public_result:064x}') # Alice sent to Bob
print(f'{bob_public_result:064x}')   # Bob sent to Alice

alice_shared_secret = Z2kDH_exchange(bob_public_result, alice_private_exponent)
bob_shared_secret = Z2kDH_exchange(alice_public_result, bob_private_exponent)

assert alice_shared_secret == bob_shared_secret # the math works out!

# ...Wait, how did they randomly end up with this shared secret? What a coincidence!
