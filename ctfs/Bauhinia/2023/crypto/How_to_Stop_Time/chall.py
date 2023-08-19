# Since the script is simple, I will just add a lot of useless information to
# distract you all. Good luck identifying whether one is a red herring!

# Although I am using the "os" package, I don't call "os.system". Now give up on
# that wacky thoughts.
import os

# I am using the `random` package, which is known to be using MT19937, a
# reversable pseudorandom number generator. Maybe you can make use of them?
import random

# I sometime receive complaints from players regarding installing random Python
# packages all around. I will refrain from using third-party packages for this
# challenge. Hope that helps!
from mathy import is_prime

def main():
    # Please do not submit "flag{this_is_a_fake_flag}" as the flag! This is only
    # a placeholder and this is not the REAL flag for the challenge. Go nc to
    # the actual server for the actual flag!
    flag = os.environ.get('FLAG', 'flag{this_is_a_fake_flag}')

    # "Once is happenstance. Twice is coincidence...
    #  Sixteen times is a recovery of the pseudorandom number generator."
    #                                       - "Maybe Someday" on Google CTF 2022
    #
    # But... How about 256 times? Prediction of pseudorandom number generator?
    for _ in range(256):
        # I will pregenerate those values ahead. Can you read that before
        # sending q?
        g = random.getrandbits(512)
        x = random.getrandbits(512)

        # Yeah, come send me a large-enough prime q!
        q = int(input('[<] q = '))

        # Told you I need a large-enough prime.
        assert q.bit_length() == 512 and is_prime(q)

        # I was going to set "p = 2*q + 1" to make p a safe prime... I will just
        # changing that to "p = 4*q + 1" to pretend that there is a bug. Let's
        # call that a... pseudo-safe prime?
        p = 4*q + 1
        assert is_prime(p)

        print(f'[>] {g = }')

        # I intentionally computes g^x mod p between printing g and h. Good luck
        # unleashing a timing attack!
        h = pow(g, x, p)

        print(f'[>] {h = }')

        # You have to recover me the "x". Quickly.
        _x = int(input('[<] x = '))
        assert x == _x

    # How should I innotate this? Go grab the flag!
    print(f'[*] {flag}')

if __name__ == '__main__':
    try:
        main()
    except:
        print('[!] Well played.')