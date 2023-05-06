import math
import random
import re
import mmh3

def randbytes(n): return bytes ([random.randint(0,255) for i in range(n)])

class BloomFilter:
    def __init__(self, m, k, hash_func=mmh3.hash):
        self.__m = m
        self.__k = k
        self.__i = 0
        self.__digests = set()
        self.hash = hash_func

    def security(self):
        false_positive = pow(
            1 - pow(math.e, -self.__k * self.__i / self.__m), self.__k)
        try:
            return int(1 / false_positive).bit_length()
        except (ZeroDivisionError, OverflowError):
            return float('inf')

    def _add(self, item):
        self.__i += 1
        for i in range(self.__k):
            self.__digests.add(self.hash(item, i) % self.__m)

    def check(self, item):
        return all(self.hash(item, i) % self.__m in self.__digests
                   for i in range(self.__k))

    def num_passwords(self):
        return self.__i

    def memory_consumption(self):
        return 4*len(self.__digests)


class PasswordDB(BloomFilter):
    def __init__(self, m, k, security, hash_func=mmh3.hash):
        super().__init__(m, k, hash_func)
        self.add_keys(security)
        self.addition_quota = 1
        self.added_keys = set()

    def add_keys(self, thresh_security):
        while self.security() > thresh_security:
            self._add(randbytes(256))
        print("Added {} security keys to DB".format(self.num_passwords()))
        print("Original size of keys {} KB vs {} KB in DB".format(
            self.num_passwords()//4, self.memory_consumption()//1024))

    def check_admin(self, key):
        if not re.match(b".{32,}", key):
            print("Admin key should be atleast 32 characters long")
            return False
        if not re.match(b"(?=.*[a-z])", key):
            print("Admin key should contain atleast 1 lowercase character")
            return False
        if not re.match(b"(?=.*[A-Z])", key):
            print("Admin key should contain atleast 1 uppercase character")
            return False
        if not re.match(br"(?=.*\d)", key):
            print("Admin key should contain atleast 1 digit character")
            return False
        if not re.match(br"(?=.*\W)", key):
            print("Admin key should contain atleast 1 special character")
            return False
        if key in self.added_keys:
            print("Admin account restricted for free tier")
            return False
        return self.check(key)

    def query_db(self, key):
        if self.check(key):
            print("Key present in DB")
        else:
            print("Key not present in DB")

    def add_sample(self, key):
        if self.addition_quota > 0:
            self._add(key)
            self.added_keys.add(key)
            self.addition_quota -= 1
            print("key added successfully to DB")
        else:
            print("API quota exceeded")


BANNER = r"""
 ____  ____  ____  ____  ____  ___  ____  ____  _  _  ____
(  _ \(_  _)( ___)( ___)( ___)/ __)(_  _)( ___)( \( )(_  _)
 )(_) )_)(_  )__)  )__)  )__)( (__  _)(_  )__)  )  (   )(
(____/(____)(__)  (__)  (____)\___)(____)(____)(_)\_) (__)

Welcome to diffecient security key database API for securely
and efficiently saving tonnes of long security keys!
Feel FREE to query your security keys and pay a little to
add your own security keys to our state of the art DB!
We trust our product so much that we even save our own keys here
"""
print(BANNER)
PASSWORD_DB = PasswordDB(2**32 - 5, 47, 768, mmh3.hash)
while True:
    try:
        option = int(input("Enter API option:\n"))
        if option == 1:
            key = bytes.fromhex(input("Enter key in hex\n"))
            PASSWORD_DB.query_db(key)
        elif option == 2:
            key = bytes.fromhex(input("Enter key in hex\n"))
            PASSWORD_DB.add_sample(key)
        elif option == 3:
            key = bytes.fromhex(input("Enter key in hex\n"))
            if PASSWORD_DB.check_admin(key):
                from flag import flag
                print(flag)
            else:
                print("No Admin no flag")
        elif option == 4:
            exit(0)
    except:
        print("Something wrong happened")
        exit(1)
