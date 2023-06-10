from Crypto.Util.number import getPrime, bytes_to_long
import os

flag = os.environ.get('FLAG', 'SEE{not_the_real_flag}').encode()

class Person:
    def __init__(self):
        p, q = getPrime(512), getPrime(512)
        self.e = 65537
        self.d = pow(self.e, -1, (p-1)*(q-1))
        self.n = p * q
    def hear(self, m): return pow(m, self.e, self.n)
    def yell(self, c): return pow(c, self.d, self.n)
        
Romeo, Juliet = Person(), Person()

noise = os.urandom(16)
print('Romeo hears the flag amidst some noise:', Romeo.hear(bytes_to_long(noise[:8] + flag + noise[8:])))

for _ in noise:
    print('Juliet hears:', Juliet.hear(Romeo.yell(int(input('Romeo yells: ')))))
    print('Romeo hears:', Romeo.hear(Juliet.yell(int(input('Juliet yells: ')))))
