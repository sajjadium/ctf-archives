#!/usr/bin/python3

import re
from Crypto.Util.number import long_to_bytes
from Crypto.Random import random
from secret import REAL_COORDS, FLAG_MSG

FAKE_COORDS = 5754622710042474278449745314387128858128432138153608237186776198754180710586599008803960884
p = 13318541149847924181059947781626944578116183244453569385428199356433634355570023190293317369383937332224209312035684840187128538690152423242800697049469987

def create_shares(secret):
    r1 = random.randint(1, p - 1)
    r2 = random.randint(1, p - 1)
    s1 = r1*r2*secret % p
    s2 = r1*r1*r2*secret % p
    s3 = r1*r2*r2*secret % p
    return [s1, s2, s3]

def reveal_secret(shares):
    s1, s2, s3 = shares
    secret = pow(s1, 3, p) * pow(s2*s3, -1, p) % p
    return secret

def run_combiner(shares):
    try:
        your_share = int(input('Enter your share: '))
        return reveal_secret([your_share, shares[1], shares[2]])
    except:
        print('Invalid share')
        exit()

def is_coords(s):
    try:
        return re.match(r'-?\d+\.\d+?, -?\d+\.\d+', long_to_bytes(s).decode())
    except:
        return False

def main():
    shares = create_shares(REAL_COORDS)
    print(f'Your share is: {shares[0]}')
    print(f'Your two friends input their shares into the combiner and excitedly wait for you to do the same...')

    secret_coords = run_combiner(shares)
    print(f'The secret is revealed: {secret_coords}')
    if not is_coords(secret_coords):
        print('"Hey those don\'t look like coordinates!"')
        print('Your friends grow a bit suspicious, but you manage to convince them that you just entered a digit wrong. You decide to try again...')
    else:
        print('"Let\'s go get the treasure!!"')
        print('Your friends run off to the revealed location to look for the treasure...')
        exit()

    secret_coords = run_combiner(shares)
    if not is_coords(secret_coords):
        print('"This is way too sus!!"')
        exit()

    if secret_coords == FAKE_COORDS:
        print('You\'ve successfully deceived your friends!')

        try:
            real_coords = int(input('Now enter the real coords: '))
            if real_coords == REAL_COORDS:
                print(FLAG_MSG)
            else:
                print('Incorrect!')
        except:
            print('Incorrect!')
    else:
        print('You are a terrible trickster!')

if __name__ == '__main__':
    main()
