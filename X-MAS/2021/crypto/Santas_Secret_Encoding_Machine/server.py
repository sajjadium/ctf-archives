import sys
import functools
import string
import binascii
from constants import *
from proof_of_work import proof_of_work
from challenge import challenge


def intro_prompt(action_count: int):
    print(f"Hello there fellow mathematician, as you well know, you have to break this encoding machine!\nAnd not only once, but {action_count} times! Good luck\n")
    sys.stdout.flush()


def invalid_input():
    print("Invalid input, closing the connection\n\n")
    sys.stdout.flush()
    exit(0)


def menu():
    print("1. Encode x^d\n2. Encode k^d\n3. Guess k\n4. Close the connection\n")
    sys.stdout.flush()
    user_input = input()
    if not user_input in ["1", "2", "3", "4"]:
        invalid_input()

    return user_input


def step_prompt(action_count: int, curr_step: int, n: int, enc_k: bytes):
    print(f"Step #{curr_step} of {action_count}, you have at most {MAX_ACTIONS} queries at your disposal!\nn = {n}\nEnc(k) = {binascii.hexlify(enc_k)}\n")
    sys.stdout.flush()


def get_decimal_input(input_name: str) -> int:
    print(f"Give me an integer in decimal form\n{input_name} = ", end="")
    sys.stdout.flush()
    user_input = input()
    is_valid = functools.reduce(lambda x, y: x and y, map(lambda x: x in string.digits, user_input))

    if not is_valid:
        invalid_input()

    return int(user_input)


def main():
    if not proof_of_work(POW_NIBBLES):
        exit(0)

    intro_prompt(ACTION_CNT)

    for i in range(ACTION_CNT):
        chall = challenge(BIT_SIZE, NO_PRIMES)

        n, k, enc_k = chall.get_challenge()
        step_prompt(ACTION_CNT, i + 1, n, enc_k)

        step_solved = False
        steps_left = MAX_ACTIONS

        while not step_solved and steps_left > 0:
            steps_left -= 1
            user_input = menu()
            if user_input == "1":
                base = get_decimal_input("x")
                exponent = get_decimal_input("d")
                print(f"Enc(x^d) = {binascii.hexlify(chall.encrypt(n, base, exponent))}\n")
                sys.stdout.flush()

            elif user_input == "2":
                exponent = get_decimal_input("d")
                print(f"Enc(x^d) = {binascii.hexlify(chall.encrypt(n, k, exponent))}\n")
                sys.stdout.flush()
            elif user_input == "3":
                candidate_k = get_decimal_input("k")

                if candidate_k == k:
                    step_solved = True
                    if i == ACTION_CNT - 1:
                        print("Well done, I'll bring you a present, wait here!\n")
                        sys.stdout.flush()
                    else:
                        print("Good, you can get to the next step!\n")
                        sys.stdout.flush()
                else:
                    print("Nope, that's not it! Such a shame, you seemed worthy...\n")
                    sys.stdout.flush()
                    exit(0)
            else:
                print("It was good to hear from you, goodbye!\n")
                sys.stdout.flush()
                exit(0)
        if step_solved == False:
            print("Well well, no more actions for you...")
            sys.stdout.flush()
            exit(0)

    print(f"Here! I found your flag: {FLAG}\n")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
