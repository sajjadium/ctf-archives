from fractions import Fraction
import ast
import base64
import hashlib
import os
import signal
import zlib

NUM_TEST = 100
TIMEOUT = 3


def timeout(_signum, _):
    print("TIMEOUT!!!")
    exit(0)


def rand():
    return int.from_bytes(os.urandom(2), "big") + 1


def gen_testcase():
    alpha, beta = rand(), rand()
    if alpha == beta:
        beta += 1
    return alpha, beta


def main():
    testcases = [gen_testcase() for _ in range(NUM_TEST)]
    print("Here are your testcases:")
    print(f"{testcases = }")

    signal.alarm(TIMEOUT)
    proof = input("proof > ")
    signal.alarm(0)

    data = base64.b64decode(input("compressed data > "))
    if hashlib.sha256(data).hexdigest() != proof:
        exit("Proof failed :(")

    data = zlib.decompress(data).decode()
    chunks = data.split('/')
    assert len(chunks) == NUM_TEST

    for (alpha, beta), chunk in zip(testcases, chunks):
        values = ast.literal_eval(chunk)
        assert len(values) == 100
        for n, (a, b, c) in zip(range(1, 101), values):
            res = (
                Fraction(a, alpha * b + beta * c) + 
                Fraction(b, alpha * c + beta * a) +
                Fraction(c, alpha * a + beta * b)
            )

            if res != n:
                exit("Wrong :(")

    print("Passed.")
    with open("./flag", "r") as f:
        flag = f.read()
        print(f"Here is the flag: {flag}")


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(TIMEOUT)
    main()
