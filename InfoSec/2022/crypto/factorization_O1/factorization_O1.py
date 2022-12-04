from Crypto.Util.number import getPrime, GCD, bytes_to_long


class RSA:

    def __init__(self, ll: int) -> None:
        self.e = 65537
        self.p, self.q = getPrime(ll // 2), getPrime(ll // 2)
        while GCD(self.e, self.p - 1) != 1 or GCD(self.e, self.q - 1) != 1 or self.p == self.q:
            self.p, self.q = getPrime(ll // 2), getPrime(ll // 2)
        self.d = pow(self.e, -1, (self.p - 1) * (self.q - 1))
        self.n = self.p * self.q

    def enc(self, x: int) -> int:
        return pow(x, self.e, self.n)

    def dec(self, y: int) -> int:
        return pow(y, self.d, self.n)


flag = b'flag{**************************************************}'
rsa = RSA(4096)
ct = rsa.enc(bytes_to_long(flag))

with open('task.txt', 'w') as f:
    f.write('e = ' + str(hex(rsa.e)) + '\n')
    f.write('n = ' + str(hex(rsa.n)) + '\n')
    f.write('ct = ' + str(hex(ct)) + '\n')



