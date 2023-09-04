import math
import mmh3


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
        return 4 * len(self.__digests)


class SocialCache(BloomFilter):
    def __init__(self, m, k, post_size=32, num_posts=16, hash_func=mmh3.hash):
        super().__init__(m, k, hash_func)
        self.post_size = post_size
        self._num_posts = num_posts

    def add_post(self, post: bytes):
        if len(post) > self.post_size:
            print("Post too long")
        elif self._num_posts <= 0:
            print("User exceeded number of allowed posts")
        else:
            self._add(post)
            self._num_posts -= 1
            print("Added successfully! Posts remaining", self._num_posts)

    def find_post(self, post: bytes):
        if self.check(post):
            print("Found the post in our DB")
        else:
            print("Could not find post in our DB")

    def grant_free_api(self):
        if self.check(b"#SEKAICTF #DEUTERIUM #DIFFECIENTWO #CRYPTO"):
            from flag import flag
            print(flag)
        else:
            print("Sorry, you dont seem to have posted about us")


BANNER = r"""
 ____  ____  ____  ____  ____  ___  ____  ____  _  _  ____  _    _  _____
(  _ \(_  _)( ___)( ___)( ___)/ __)(_  _)( ___)( \( )(_  _)( \/\/ )(  _  )
 )(_) )_)(_  )__)  )__)  )__)( (__  _)(_  )__)  )  (   )(   )    (  )(_)(
(____/(____)(__)  (__)  (____)\___)(____)(____)(_)\_) (__) (__/\__)(_____)
Welcome to diffecientwo caching database API for tracking and storing
content across social media. We have repurposed our security product as
saving the admin key was probably not the best idea, but we have decided
to change our policies and to achieve better marketing, we are offering
free API KEY to customers sharing #SEKAICTF #DEUTERIUM #DIFFECIENTWO #CRYPTO
on LonelyFans (our premium business partner).
"""
print(BANNER)
LONELY_FANS = SocialCache(2**32 - 5, 64, 32, 22)
while True:
    try:
        option = int(input("Enter API option:\n"))
        if option == 1:
            post = bytes.fromhex(input("Enter post in hex\n"))
            LONELY_FANS.find_post(post)
        elif option == 2:
            post = bytes.fromhex(input("Enter post in hex\n"))
            LONELY_FANS.add_post(post)
        elif option == 3:
            LONELY_FANS.grant_free_api()
        elif option == 4:
            exit(0)
    except BaseException:
        print("Something wrong happened")
        exit(1)
