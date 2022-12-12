from secrets import token_bytes
from itertools import cycle

FLAG = open("flag.txt", "rb").read().split(b'\n')

wee = token_bytes(8)
cipher = ''

for secret in FLAG:
	enc = bytes([ a ^ b for a,b in zip(secret, cycle(wee)) ])
	cipher += enc.hex() + '\n'

open("flag.enc", "w").write(cipher)