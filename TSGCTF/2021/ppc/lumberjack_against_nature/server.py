from mpmath import power, ln
from random import SystemRandom
from string import ascii_letters
from signal import alarm

from secret import decode_fast, flag

alarm(10)

def to_string(number):
	return number.to_bytes((number.bit_length() + 7) // 8, 'big')[:74]
def decode(enc):
	return to_string(int(power(2, enc * ln(2))))

assert(decode(1337 << 5) == decode_fast(1337, 5))


plaintext = ''.join(SystemRandom().choice(ascii_letters) for _ in range(74)).encode()
e = 13371337

print(f'decode(s << {e}) == {plaintext}')
s = int(input('s = ? '))

if 0 < s < 2 ** (75 * 8) and decode_fast(s, e) == plaintext:
	print(f'Congrats! {flag}')
else:
	print(":P")
