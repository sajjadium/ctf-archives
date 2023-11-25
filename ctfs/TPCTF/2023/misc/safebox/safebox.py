
from Crypto.Cipher import ChaCha20
from hashlib import sha256
from itertools import cycle
from pathlib import Path
import os

from secret import flag

CHACHA20_KEY = b'3gn8C5j9PedPqf2tKANb91c5k5cxXx2n'

CONTENT_SIZE = 32
IV_SIZE = 12
BLOCK_SIZE = CONTENT_SIZE + IV_SIZE


def encrypt_block(data, key, key2):
    iv = os.urandom(IV_SIZE)
    cipher = ChaCha20.new(key=CHACHA20_KEY, nonce=iv)
    return iv + cipher.encrypt(bytes([(x + (y ^ z)) & 0xff for x, y, z in zip(data, cycle(key), cycle(key2))]))

def decrypt_block(block, key, key2):
    cipher = ChaCha20.new(key=CHACHA20_KEY, nonce=block[:IV_SIZE])
    return bytes([(x - (y ^ z)) & 0xff for x, y, z in zip(cipher.decrypt(block[IV_SIZE:]), cycle(key), cycle(key2))])


class IncorrectKeyException(Exception):
    pass


class SafeFS:
    def __init__(self, base, secret_key):
        self.base = Path(base)
        self.secret_key = secret_key
        self.file_key_hashes = {}
        self.total_written = 0

    def _path(self, path):
        return self.base / sha256(path).hexdigest()

    def _open(self, path, mode, key):
        key_hash = sha256(key).digest()
        if path in self.file_key_hashes:
            if self.file_key_hashes[path] != key_hash:
                raise IncorrectKeyException

        self.file_key_hashes[path] = key_hash

        key2 = sha256(self.secret_key + path).digest()
        path = self._path(path)
        if not path.exists():
            path.touch()
        return open(path, mode), key2

    def read(self, path, offset, length, key):
        file, key2 = self._open(path, 'rb', key)

        result = b''
        blk, rem = divmod(offset, CONTENT_SIZE)
        while len(result) < length:
            file.seek(blk * BLOCK_SIZE)
            block = file.read(BLOCK_SIZE)
            if len(block) == 0:
                break
            result += decrypt_block(block, key, key2)[rem:]

            blk += 1
            rem = 0

        return result[:length]

    def write(self, path, offset, data, key):
        file, key2 = self._open(path, 'rb+', key)

        self.total_written += len(data)
        if self.total_written > 20 * 1024 * 1024:
            print('You\'ve exceeded the storage limit!')
            quit()

        written = 0
        blk, rem = divmod(offset + written, CONTENT_SIZE)
        while len(data) > 0:
            off = blk * BLOCK_SIZE
            file.seek(off)
            block = file.read(BLOCK_SIZE)
            if len(block) != 0:
                block = decrypt_block(block, key, key2)

            count = min(CONTENT_SIZE - rem, len(data))
            block = bytearray(block.ljust(rem + count, b'\0'))
            block[rem:rem + count] = data[:count]
            data = data[count:]
            written += count

            file.seek(off)
            file.write(encrypt_block(block, key, key2))

            blk += 1
            rem = 0

    def rename(self, old, new):
        if old == new:
            return

        # TODO: renaming file corrupts it
        self._path(old).rename(self._path(new))
        self.file_key_hashes[new] = self.file_key_hashes[old]
        del self.file_key_hashes[old]

    def remove(self, path):
        self._path(path).unlink()
        del self.file_key_hashes[path]


BANNER = '''
🔒 Welcome to the Safebox! 🔒

Each file is encrypted with a separate
key, making the system super duper safe.

Make sure you don't forget the keys ;)

Commands:
  get [file] [offset] [length] [key]
  put [file] [offset] [data] [key]
  mv [old] [new]
  rm [file]
  exit

Binary data is encoded in hex.

Example:
  put secret.txt 0 0x0123456789 secretkey
  get secret.txt 0 5 secretkey
    - 0123456789
'''

print(BANNER)

fs = SafeFS('./base', os.urandom(32))

def process_command(cmd, args):
    if cmd == 'get':
        file, offset, length, key = args
        if file.endswith(b'.flag'):
            print('Nope')
            return

        data = fs.read(file, int(offset), int(length), key)
        print(data.hex())

    elif cmd == 'put':
        file, offset, data, key = args
        fs.write(file, int(offset), data, key)

    elif cmd == 'mv':
        old, new = args
        fs.rename(old, new)

    elif cmd == 'rm':
        file, = args
        fs.remove(file)

    elif cmd == 'putflag':
        # TODO: remove
        file, key = args
        fs.write(file + b'.flag', 0, flag, key)

    elif cmd == 'exit':
        print('Bye!')
        quit()

    else:
        print('Unknown command')

while True:
    line = input('> ').strip().split()
    if len(line) == 0:
        continue
    args = [bytes.fromhex(x[2:]) if x.startswith('0x')
            else x.encode() for x in line[1:]]

    try:
        process_command(line[0], args)
    except IncorrectKeyException:
        print('Incorrect key')
