from hashlib import sha256
from random import choice
from string import digits, ascii_letters

alphabet = (digits + ascii_letters).encode()
def random(len):
    return bytes(choice(alphabet) for _ in range(len))

class PoW(object):
    def __init__(self, lvl : int = 4, nonce_size : int = 16, hashFn = sha256):
        self.hashFn = hashFn
        self.lvl = lvl
        self.nonce = random(nonce_size)
    
    def generate_tag(self, prefix : bytes):
        assert len(prefix) == self.lvl
        return self.hashFn(prefix+self.nonce).digest()
    
    def generate(self):
        return self.nonce, self.generate_tag(random(self.lvl))
    
    def validate(self, secret : bytes, digest : bytes):
        return digest == self.generate_tag(secret)
