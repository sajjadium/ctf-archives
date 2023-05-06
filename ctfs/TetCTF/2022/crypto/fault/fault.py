from secrets import randbits
from Crypto.Util.number import getPrime  # pycryptodome

NBITS = 1024
D_NBITS = 128  # small `d` makes decryption faster


class Cipher:
    def __init__(self):
        p = getPrime(NBITS // 2)
        q = getPrime(NBITS // 2)
        self.n = p * q
        self.d = getPrime(D_NBITS)
        self.e = pow(self.d, -1, (p - 1) * (q - 1))

    def encrypt(self, m: int) -> int:
        assert m < self.n
        return pow(m, self.e, self.n)

    def faultily_decrypt(self, c: int):
        assert c < self.n
        fault_vector = randbits(D_NBITS)
        return fault_vector, pow(c, self.d ^ fault_vector, self.n)


def main():
    from secret import FLAG
    cipher = Cipher()
    c = cipher.encrypt(int.from_bytes(FLAG.encode(), "big"))

    for _ in range(2022):
        line = input()
        print(cipher.faultily_decrypt(c if line == 'c' else int(line)))


if __name__ == '__main__':
    main()
