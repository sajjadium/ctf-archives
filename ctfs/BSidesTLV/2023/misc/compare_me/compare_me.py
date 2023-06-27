import os
import sys

from ctypes import CDLL, c_char_p, c_uint32

# memcmp_all to ensure constant time check
memcmp_all = CDLL('./memcmp_all.so').memcmp_all
memcmp_all.argtypes = [c_char_p, c_char_p, c_uint32]
memcmp_all.restype = c_uint32

def main():
    guess_me = os.urandom(16)
    flag = os.getenv("FLAG")
    print("Wellcome!")
    print("I have choosen a 128-bit random.")
    print("See if you can guess it with just 20 queries.")
    print("You can enter an empty line to exit.")
    for turn in range(20):
        req = input(f"\n(guess {turn+1} out of 20) Your input: ")
        if len(req) == 0:
            return
        if len(req) != 32:
            print(f'Bad input length {len(req)} != 32')
            continue
        guess = bytes.fromhex(req)
        ret = memcmp_all(guess_me, guess, 16)
        if ret == 0:
            print(f'Success! {flag}')
        else:
            print(f'Wrong! {ret} is not zero!')
    print("Too many attempts!")

if __name__ == "__main__":
    try:
        main()
        print("Bye!")
    except:
        print("Some error occured")
    sys.exit(0)
