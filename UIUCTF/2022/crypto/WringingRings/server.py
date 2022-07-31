import sympy as sp
import random
import signal
from secret import FLAG

secret = random.SystemRandom().randint(1, 500_000)

_MAX = 10 ** (len(str(secret)) - 1)

# generating a polynomial
def _f(secret, minimum=3):
    coeffs = [secret] + [
        random.SystemRandom().randint(1, _MAX) for _ in range(minimum - 1)
    ]

    # print("Secret Polynomial:")
    # f_str = str(secret)
    # for i, coeff in enumerate(coeffs[1:]):
    #     f_str += " + " + str(coeff) + "*x^" + str(i + 1)
    # print(f_str)

    def f(x):
        res = 0
        for i, coeff in enumerate(coeffs):
            res += coeff * x ** (i)

        return res

    return f


def gen_shares(secret, minimum=3):
    f = _f(secret, minimum)
    shares = [(i + 1, f(i + 1)) for i in range(minimum)]
    return shares


def challenge(secret, minimum=3):
    shares = gen_shares(secret, minimum)
    points = random.sample(shares, minimum - 1)
    points.sort()
    return points


def main():
    minimum = 10
    points = challenge(secret, minimum)

    print("[SSSS] Known shares of the secret polynomial: ")
    for point in points:
        print(f"       {point}")
    print()
    
    signal.alarm(60)
    guess = int(input("[SSSS] Enter my secret: "))
    if guess == secret:
        print(f"[SSSS] Correct! {FLAG}")
    else:
        print("[SSSS] Incorrect...")
    
if __name__ == "__main__":
    main()
