import math
from Crypto.Hash import CMAC
from Crypto.Util.number import long_to_bytes, getPrime, bytes_to_long, isPrime
from Crypto.Cipher import AES
from hidden import power_tower_mod, flag

assert bytes_to_long(flag).bit_length() == 1263

"""
    power_tower_mod -> takes x, n and some data and returns
                   .
                  .
                 .
                x          
               x
              x 
             x            
            x                 mod n
        i.e. infinite power tower of x modulo n
        x^(x^(x^(x^(x.......))))) mod n
        There are no vulnerabilities in that function trust me!!
"""

class bigMac:
    def __init__(self, security = 1024):

        self.security = security
        self.n, self.data = self.generator()
        self.base = getPrime(security) * getPrime(security)
        self.message = bytes_to_long(flag)
        self.process()
        self.verified = False

        self.bits = 96
        self.keys = []
        for i in range(self.bits):
            self.keys.append(getPrime(self.bits))

        print("My m4c&ch3353:", self.mac)
        print("My signature: ", self.getSignature(self.base))

        self.next()

    def generator(self):
        chunk = 128
        while 1:
            data = []
            n = 1
            for i in range(2 * self.security // chunk):
                data.append([getPrime(chunk), 1])
                n *= data[-1][0]
            data.append([2, 2 * self.security - n.bit_length()])
            while n.bit_length() < 2 * self.security:
                n *= 2
            if n.bit_length() == 2 * self.security:
                return n, data

    def process(self):
        x = long_to_bytes(self.n)
        cc = CMAC.new(x[:16], ciphermod=AES)
        self.mac = cc.update(x).hexdigest()

    def getSignature(self, toSign):
        return (toSign * toSign) % (1 << (toSign.bit_length() - (self.security // 250)))

    def verify(self, N, data):
        self.next()
        if self.verified:
            print("ALREADY VERIFIED")
            return False
        if N.bit_length() != 2 * self.security:
            print("size of N is not correct.")
            return False

        prev = self.n
        mac = self.mac
        self.n = N
        self.process()
        x = 1
        maxPrime = 0
        for i in range(len(data)):
            data[i][0] = int(data[i][0])
            data[i][1] = int(data[i][1])
            if not isPrime(data[i][0]):
                self.n = prev
                self.mac = mac
                print("Gimme primesssssss onlyyyy!!")
                return False
            x *= pow(data[i][0], data[i][1])
            maxPrime = max(maxPrime, data[i][0])

        if self.mac != mac or x != N or maxPrime.bit_length() > self.security // 5:
            self.n = prev
            self.mac = mac
            print("Failed to verify.")
            return False


        print("Yayyyyyyyy! big mac got verified! for n =", prev)
        print("Data =", self.data)

        self.data = data
        self.n = N

        self.verified = True
        return True


    def next(self):
        self.base = power_tower_mod(self.base, self.data, self.n)


    def obfuscateSmall(self, m):
        obs = m & ((1 << self.bits) - 1)
        m ^= obs
        final = 0
        for i in range(self.bits):
            if ((obs >> i) & 1):
                final += self.keys[i]

        return m + final

    def communicate(self):
        self.next()
        if self.verified:
            x = self.obfuscateSmall(bytes_to_long(flag))
            while math.gcd(x, n) != 1:
                x += 1
            while math.gcd(self.base, self.n) != 1:
                self.base += 1
            print(f"Here is your obfuscated c: {pow(x, self.base, self.n)}")
        else:
            print("Verification needed.")

    def power_tower(self, x):
        self.next()
        if self.verified:
            print("WTF(What a Freak), you have n do it yourself.")
            return -1
        return power_tower_mod(x, self.data, self.n)

if __name__ == "__main__":
    big = bigMac()

    steps = 90
    while steps > 0:
        print("1: Communicate.")
        print("2: Verify.")
        print("3: Obfuscating.")
        print("4: Quit.")

        steps -= 1

        x = int(input("Choose: "))
        if x == 1:
            big.communicate()
        elif x == 2:
            n = int(input("Give me the MY modulus : "))
            *inp, = input("Enter prime factorization in format [prime1, count1]-[prime2, count2]-[...: ").split('-')
            data = []
            for i in inp:
                curr = i[1:-1].split(", ")
                data.append([int(curr[0]), int(curr[1])])
            big.verify(n, data)
        elif x == 3:
            x = int(input("Enter your message : "))
            print("Here is your obfuscated message : ", big.obfuscateSmall(x))
        elif x == 4:
            print("Goodbye.")
            quit()
        else:
            print("Wrong input.")