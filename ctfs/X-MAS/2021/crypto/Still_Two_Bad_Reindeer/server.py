import functools
import os
import sys
import string
import binascii
from constants import *
from proof_of_work import proof_of_work
from challenge import hash_func


def intro_prompt():
    print("Randolf: OK, ok... so our first cipher was bad because the xor didn't produce enough randomness"
          "and the key-dependent shifts were not strong enough!")
    print("Xixen: Since then, we decided on making a hash function, it's easy to design hash functions, right?")
    print("Randolf: If you manage to find a string that has an arbitrary value that we choose, we will reward you "
          "again and just give up")
    print(f"Xixen: We are very confident that this time you will not succeed! You'll also have to prove that the "
          f"exploit is consistent so you will have to do it {ACTION_COUNT} times.\nAlso, you can't try more than "
          f"{STEP_COUNT} strings to be hashed for each exploit instance. Good luck!\n")
    sys.stdout.flush()


def invalid_input():
    print("Invalid input, closing the connection\n\n")
    sys.stdout.flush()
    exit(0)


def step_prompt(step):
    print(f"Step #{step} of {ACTION_COUNT}\n")
    sys.stdout.flush()


def get_hexadecimal_input(input_name):
    print(f"Give me an integer in hexadecimal format\n{input_name} = ", end="")
    sys.stdout.flush()
    user_input = input()
    is_valid = functools.reduce(lambda x, y: x and y, map(lambda x: x in string.hexdigits, user_input))

    if not is_valid:
        invalid_input()

    return binascii.unhexlify(user_input)


def challenge_prompt(hash_result):
    print(f"Please find a string that when encrypted has the following hash:\n\nhash(string) = {binascii.hexlify(hash_result)}\n")


def main():
    if not proof_of_work(POW_NIBBLES):
        exit(0)

    intro_prompt()

    for i in range(ACTION_COUNT):
        key = os.urandom(KEY_SIZE // 8)
        salt = os.urandom(BLOCK_SIZE // 8)
        hash_result = os.urandom(BLOCK_SIZE // 8)
        steps_left = STEP_COUNT

        step_prompt(i + 1)
        challenge_prompt(hash_result)

        while steps_left > 0:
            print(f"You have {steps_left} steps left!")

            user_input = get_hexadecimal_input("string")

            if hash_func(salt, user_input, key) == hash_result:
                print("Ok you did it, but that was just a lucky guess")
                sys.stdout.flush()
                break
            else:
                print("Nope, that was not correct, sorry!")
                sys.stdout.flush()

            steps_left -= 1

        if steps_left == 0:
            print("Sorry, you are out of moves! Seems like we were right, the hash function is perfect!")
            sys.stdout.flush()
            exit(0)

    print(f"Fine, you have bested us! Here's your flag: {FLAG}\n")
    sys.stdout.flush()


if __name__ == '__main__':
    main()
