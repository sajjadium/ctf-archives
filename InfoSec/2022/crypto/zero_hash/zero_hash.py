from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.number import bytes_to_long


def hash_func(msg: bytes, offset: int, prime: int, size: int) -> int:
    h = offset
    for i in range(0, len(msg)):
        h ^= msg[i]
        h = (h * prime) % size
    return h


with open('data.txt', 'r') as f:
    hash_offset = int(f.readline(), 16)
    hash_prime = int(f.readline(), 16)
    hash_size = int(f.readline(), 16)

x = bytes_to_long(b'some_secret_integer_value')

zero_msg = bytearray()
zero_msg.append(0x06)
[zero_msg.append(0x00) for _ in range(x)]
zero_msg.append(0x01)
assert hash_func(bytes(zero_msg), hash_offset, hash_prime, hash_size) == 0

key = SHA256.new(str(len(zero_msg)).encode()).digest()
aes = AES.new(key, AES.MODE_CTR)

with open('../dev/flag.txt', 'r') as f:
    flag = bytes(f.readline(), 'ascii')

with open('task.txt', 'w') as f:
    f.write(aes.encrypt(flag).hex() + '\n')
    f.write(aes.nonce.hex() + '\n')
