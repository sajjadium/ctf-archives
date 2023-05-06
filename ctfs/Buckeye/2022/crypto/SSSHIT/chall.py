import Crypto.Util.number as cun
import random
import ast


def evaluate_polynomial(polynomial: list, x: int, p: int):
    return (
        sum(
            (coefficient * pow(x, i, p)) % p for i, coefficient in enumerate(polynomial)
        )
        % p
    )


N_SHARES = 3


def main():
    print(
        f"I wrote down a list of people who are allowed to get the flag and split it into {N_SHARES} using Shamir's Secret Sharing."
    )
    MESSAGE = cun.bytes_to_long(b"qxxxb, BuckeyeCTF admins, and NOT YOU")

    p = cun.getPrime(512)

    polynomial = [MESSAGE] + [random.randrange(1, p) for _ in range(N_SHARES - 1)]
    points = [(i, evaluate_polynomial(polynomial, i, p)) for i in range(1, N_SHARES + 1)]

    print("Your share is:")
    print(points[0])
    print("The other shares are:")
    for i in range(1, len(points)):
        print(points[i])

    print()
    print("Now submit your share for reconstruction:")
    your_input = ast.literal_eval(input(">>> "))
    if (
        type(your_input) is not tuple
        or len(your_input) != 2
        or type(your_input[0]) is not int
        or type(your_input[1]) is not int
        or your_input[0] != 1
        or not (0 <= your_input[1] < p)
    ):
        print("Bad input")
        return

    points[0] = your_input

    xs = [point[0] for point in points]
    ys = [point[1] for point in points]

    y_intercept = 0
    for j in range(N_SHARES):
        product = 1
        for i in range(N_SHARES):
            if i != j:
                product = (product * xs[i] * pow(xs[i] - xs[j], -1, p)) % p
        y_intercept = (y_intercept + ys[j] * product) % p

    reconstructed_message = cun.long_to_bytes(y_intercept)
    if reconstructed_message == b"qxxxb, BuckeyeCTF admins, and ME":
        print("Here's your flag:")
        print("buckeye{?????????????????????????????????????????}")
    else:
        print(f"Sorry, only these people can see the flag: {reconstructed_message}")


main()
