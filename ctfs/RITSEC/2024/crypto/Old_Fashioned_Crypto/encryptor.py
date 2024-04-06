import json
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from math import gcd, log2, ceil


class CryptoSystem:
    def __init__(self, size, pub_key=None, priv_key=None):
        self.size = size
        if pub_key is None and priv_key is None:
            self._gen_keys()
        elif pub_key is None:
            self.priv_key = priv_key
            self._prv_lst, self._prv_q, self._prv_r, self._prv_r_inv = self.priv_key
            self._gen_pub_key()
        else:
            self.priv_key = priv_key
            if self.priv_key is not None:
                self._prv_lst, self._prv_q, self._prv_r, self._prv_r_inv = self.priv_key
            self.pub_key = pub_key

    def _gen_keys(self):
        lst = []
        total = 0
        for i in range(self.size):
            nxt = total + sum(get_random_bytes(4))
            total += nxt
            lst.append(nxt)
        self._prv_lst = lst
        self._prv_q = total + sum(get_random_bytes(4))
        self._prv_r = 0
        while gcd(self._prv_r, self._prv_q) != 1:
            self._prv_r = sum(get_random_bytes(8))
        self._inv(self._prv_r, self._prv_q)
        self.priv_key = (self._prv_lst, self._prv_q, self._prv_r, self._prv_r_inv)
        self._gen_pub_key()

    def _inv(self, a, b):
        x, y = self._inv_help(a, b)
        self._prv_r_inv = x + b if x < 0 else x

    def _inv_help(self, a, b):
        if a == 1 and b == 0:
            return 1, 0
        x_p, y_p = self._inv_help(b, a % b)
        x = y_p
        y = x_p - y_p * (a // b)
        return x, y

    def _gen_pub_key(self):
        self.pub_key = [(self._prv_r * w) % self._prv_q for w in self._prv_lst]

    def encrypt(self, data):
        if len(data) * 8 > self.size:
            raise ValueError(f"Data too big! Data has {len(data)*8} bits, can only encrypt {self.size} bits")
        val = int.from_bytes(data, 'big')
        tot = 0
        for i in range(self.size):
            if val & (1 << (self.size - 1 - i)):
                tot += self.pub_key[i]
        return tot.to_bytes(ceil(log2(tot)/8), 'big')

    def decrypt(self, ct):
        if self.priv_key is None:
            raise ValueError('This instance not created with private key; Cannot decrypt!')
        inv = (int.from_bytes(ct, 'big') * self._prv_r_inv) % self._prv_q
        data = 0
        for i in range(self.size-1, -1, -1):
            if self._prv_lst[i] <= inv:
                inv -= self._prv_lst[i]
                data |= (1 << (self.size - 1 - i))
        return data.to_bytes(self.size//8, 'big')


def main():
    n = 128
    c = CryptoSystem(n)
    key = get_random_bytes(n//8)
    enc_key = c.encrypt(key)
    iv = get_random_bytes(n//8)
    sym_c = AES.new(key, mode=AES.MODE_CBC, iv=iv)
    with open('flag.txt', 'rb') as f:
        flag = f.read()
    enc_flag = sym_c.encrypt(pad(flag, AES.block_size))
    with open('output.json', 'w') as f:
        json.dump({'enc_flag': enc_flag.hex(), 'enc_key': enc_key.hex(), 'pub_key': c.pub_key, 'iv': iv.hex()}, f)


if __name__ == '__main__':
    main()
