from secret import SUPERBOX, key, flag
from hashlib import sha512
from sys import argv

try:
    assert set(SUPERBOX) == set(range(3 ^ 5))
    assert sha512(str(list(SUPERBOX)).encode()).hexdigest() == "ec7c27e69f323ae28e9321b50b99ecdcebc208c2d1d5ad48e53ae1416b3e38ddb9d6cb1977bd88b75e8d464baae398a8c6f5ce4fba3ae716bd523474126031a1"
    assert SUPERBOX[13] == 37 # Patented identification method
except:
    print("INVALID SUPERBOX SUPPLIED.")
    print("CONTACT YOUR SUPERVISOR FOR A NEW COPY.")
    exit()

class Expansion:
    F.<a> = GF(3 ^ 5, modulus = x^5 + x^3 + x + 1)
    G.<b> = PolynomialRing(F)
    H.<c> = G.quo(b ^ 3 - 1)
    CONSTANT = a^4 * c^2 + a^2 * c + a

    PBOX = [2, 3, 7, 4, 8, 0, 6, 1, 5]

    def __init__(self, primary_key):
        assert len(primary_key) == 45
        slices = [primary_key[i:i + 5] for i in range(0, 45, 5)]
        self.primary_key = [Expansion.F.from_integer(ZZ(i, 3)) for i in slices]

    @staticmethod
    def mix(x):
        x2 = sum(j * Expansion.c ^ i for i, j in enumerate(x))
        result = x2 * Expansion.CONSTANT
        return [result[i] for i in range(3)]

    def generate(self, n):
        new_key = [Expansion.F.from_integer(n)] * 9
        new_key = [i + j for i, j in zip(new_key, self.primary_key)]

        for _ in range(2):
            new_key = [new_key[i] for i in Expansion.PBOX]
            new_key = sum((Expansion.mix(new_key[i:i + 3]) for i in range(0, 9, 3)), [])
            # Patented diffusion technology
            tmp = [Expansion.F.from_integer(SUPERBOX[i.to_integer()]) for i in new_key]
            new_key = [i * (j^2 + Expansion.a^2) * j for i, j in zip(tmp, new_key)]
            new_key = [i + j for i, j in zip(new_key, self.primary_key)]

        output = []
        for n in new_key:
            output.extend([n[i] for i in range(5)])
        return output

    def expand(self, n = 17 * 45):
        keys = []
        for i in range(n // 45 + 1):
            keys.extend(self.generate(i))
        return keys[:n]

def bytes_to_trits(inp):
    tmp = int.from_bytes(inp, byteorder='little')
    tmp = Integer(tmp).digits(3)
    return tmp

def trits_to_bytes(inp, size = None):
    tmp = ZZ(inp, 3)
    tmp = int(tmp)
    if size is None: size = (tmp.bit_length() + 7) // 8
    tmp = tmp.to_bytes(size, "little")
    return tmp

def pad(x, n):
    if isinstance(x, bytes): fill = b"\x00"
    elif isinstance(x, list): fill = [0]
    else: raise Exception
  
    return x + fill * (n - len(x))

class SuperEncrypt:
    F.<a> = GF(3 ^ 135, 'a')
    f = lambda x: sum(j * SuperEncrypt.a ^ i for i, j in enumerate(x))

    def __init__(self, primary_key):
        keys = Expansion(primary_key).expand()
        keys = [keys[i:i + 135] for i in range(0, len(keys), 135)]
        self.keys = list(map(SuperEncrypt.f, keys))

    def encrypt(self, message):
        assert len(message) == 270

        left, right = SuperEncrypt.f(message[:135]), SuperEncrypt.f(message[135:])

        for k in self.keys:
            right += (k + left) ^ 2
            left, right = right, left

        return [left[i] for i in range(135)] + [right[i] for i in range(135)]

    def decrypt(self, message):
        assert len(message) == 270

        left, right = SuperEncrypt.f(message[:135]), SuperEncrypt.f(message[135:])

        for k in self.keys[::-1]:
            left, right = right, left
            right -= (k + left) ^ 2

        return [left[i] for i in range(135)] + [right[i] for i in range(135)]

    def encrypt_message(self, message: bytes) -> bytes:
        message_hash = pad(bytes_to_trits(sha512(message).digest()[:25]), 135)

        output = []
        for i in range(0, len(message), 25):
            chunk = pad(bytes_to_trits(message[i:i + 25] + b"\xff"), 135)
            chunk = self.encrypt(chunk + message_hash)
            chunk = pad(trits_to_bytes(chunk), 54)
            output.append(chunk)

        return b"".join(output)

    def decrypt_message(self, message: bytes) -> bytes:
        output = []
        for i in range(0, len(message), 54):
            chunk = pad(bytes_to_trits(message[i:i + 54]), 270)
            chunk = self.decrypt(chunk)
            chunk = trits_to_bytes(chunk[:135])[:-1]
            output.append(chunk)

        return b"".join(output)

def main():
    E = SuperEncrypt(key)
    source = argv[1]

    with open(source, "rb") as f:
        contents = f.read()[:6000] # stop from exploding

    print(f"Loaded up to 6000 bytes: {source}")
    encrypted_contents = E.encrypt_message(contents)
    print(f"Encrypted.")
    destination = source + ".enc"

    with open(destination, "wb+") as f:
        f.write(encrypted_contents)

    print(f"Saved: {destination}")

    hidden_flag = bytes(i ^^ j for i, j in zip(flag, sha512(str(list(key)).encode()).digest()))

    print(f"Think you have the key? {hidden_flag}")

if __name__ == "__main__":
    main()
