import signal
import os
import sys
import random
from Crypto.Util.number import isPrime as is_prime


def tle_handler(*args):
    print('⏰')
    sys.exit(0)


def main():
    # Just to make sure the order is large enough
    p = 0xde5831cd21036cbbf072deac86ac1a48f74e3e78bcd916132cf54ee27a80e26021cd0371c698c35ddb6927fdf184a8345c562c4d59d35806177b7931d64390694d105d62a9a67fbf509148a0ab639048b7b6aa6439f31c499006b97d7b2dc4fd7376c0e66dae9972f42d4be2fe835d76cc94a0ecc585009d967fcc7de05cb177
    q = 0x6f2c18e69081b65df8396f5643560d247ba71f3c5e6c8b09967aa7713d40713010e681b8e34c61aeedb493fef8c2541a2e2b1626ace9ac030bbdbc98eb21c834a6882eb154d33fdfa848a45055b1c8245bdb55321cf98e24c8035cbebd96e27eb9bb607336d74cb97a16a5f17f41aebb664a507662c2804ecb3fe63ef02e58bb
    g = 2
    assert is_prime(p)
    assert is_prime(q)
    assert p == 2*q + 1
    assert pow(g, q, p) == 1

    signal.signal(signal.SIGALRM, tle_handler)
    signal.alarm(3600)

    flag = os.environ.get('FLAG', 'firebird{***REDACTED***}')

    x = random.getrandbits(48)
    y = pow(g, pow(g, x, q), p)
    print(f'💬 {y}')
    _x = int(input('🥺 '))
    assert x == _x

    print(f'🏁 {flag}')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print('😒')
