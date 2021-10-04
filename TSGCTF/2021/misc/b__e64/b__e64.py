import random
import string
import base64
import os


def gen_chal():
    cs = string.ascii_lowercase + string.digits
    return ''.join(random.choices(cs, k=32))


def enc(s, encoding='ascii'):
    for _ in range(8):
        s = base64.b64encode(bytes(s, encoding)).decode(encoding)
    return s


def main():
    # receive a mask
    mask = input('mask: ')
    if len(mask) != 344 or any(c not in '*?' for c in mask):
        print('bad mask :(')
        return
    if mask.count('?') > 124:
        print("don't be too greedy!")
        return

    for q in range(1, 9):
        # generate a challenge
        secret = gen_chal()
        encoded = enc(secret)
        assert len(encoded) == 344

        # give them the masked secret
        masked = ''.join('*' if m == '*' else c for m, c in zip(mask, encoded))
        print(f'Q{q}: {masked}')

        # let them guess the secret
        guess = input(f'A{q}: ')
        if secret != guess:
            print('you lose!')
            print(f'secret: {secret}')
            return
        else:
            print("correct!")

    print('you win!')
    print(f"flag: {os.environ.get('FLAG')}")


if __name__ == '__main__':
    main()
