from .table import reverse_table, table


def mangle(key_bytes: bytes, value_bytes: bytes) -> bytes:
	key = list(key_bytes)
	value = list(value_bytes)

	value = mix(key, value)
	value = shift(value)
	value = mix(key, value)
	value = shift(value)
	value = mix(key, value)
	value = tabulate(value)
	value = shift(value)
	value = mix(key, value)
	value = tabulate(value)
	value = shift(value)
	value = mix(key, value)
	value = shift(value)
	value = mix(key, value)

	return bytes(value)

def unmangle(key_bytes: bytes, value_bytes: bytes) -> bytes:
	key = list(key_bytes)
	value = list(value_bytes)

	value = unmix(key, value)
	value = unshift(value)
	value = unmix(key, value)
	value = unshift(value)
	value = untabulate(value)
	value = unmix(key, value)
	value = unshift(value)
	value = untabulate(value)
	value = unmix(key, value)
	value = unshift(value)
	value = unmix(key, value)
	value = unshift(value)
	value = unmix(key, value)

	return bytes(value)

def mix(key: list[int], value: list[int]) -> list[int]:
	last = 0
	ret: list[int] = value.copy()
	for i in range(len(value)):
		ret[i] ^= key[i]
		ret[i] ^= last
		last = value[i]
	return ret

def unmix(key: list[int], value: list[int]) -> list[int]:
	last = 0
	ret: list[int] = value.copy()
	for i in range(len(value)):
		ret[i] ^= last
		ret[i] ^= key[i]
		last = ret[i]
	return ret

def shift(value: list[int]) -> list[int]:
	ret = value.copy()
	ret[0] ^= ret[-1]
	return ret

unshift = shift

def tabulate(value: list[int]) -> list[int]:
	ret = value.copy()
	for i in range(len(value)):
		ret[i] = table[ret[i]]
	return ret

def untabulate(value: list[int]) -> list[int]:
	ret = value.copy()
	for i in range(len(value)):
		ret[i] = reverse_table[ret[i]]
	return ret
