#!/usr/bin/env -S python3 -u

import secrets
import codecs
import time

def get_flag():
    with open("/tmp/pw_flag", 'rt') as f:
        print(f.read())

# initialize password
def init_password():
    global password
    global sample_password
    # seems super secure, right?
    password = "%08x" % secrets.randbits(32)
    sample_password = "%08x" % secrets.randbits(32)


# the function that matters..
def guess_password(s):
    print("Password guessing %s" % s)
    typed_password = ''
    correct_password = True
    for i in range(len(password)):
        user_guess = input("Guess character at position password[%d] = %s?\n" \
                % (i, typed_password))
        typed_password += user_guess
        if user_guess != password[i]:
            # punish the users for supplying wrong char..
            time.sleep(0.3 * (int(password[i], 16)+1))
            correct_password = False

    # to get the flag, please supply all 8 correct characters for the password..
    if correct_password:
        get_flag()

    return correct_password   

def calibrate():
    print("Press enter to begin a 1 second delay.")
    input()
    time.sleep(1)
    print("1 second has passed")

if __name__ == '__main__':
    init_password()
    print("Can you tell me what my password is?")
    print("We randomly generated 8 hexadecimal digit password (e.g., %s)" % sample_password)
    print("so please guess the password character by character.")
    print("You have only 2 chances to test your guess...")
    while True:
        print()
        print("Menu:")
        print("(1) Calibrate Timing")
        print("(2) Guess Password")
        x = input()
        if '1' in x:
            calibrate()
        if '2' in x:
            break
    guess_password("Trial 1")
    if not guess_password("Trial 2"):
        print("My password was %s" % password)
