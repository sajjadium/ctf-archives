import random
from secret import flag, fast_exp
import signal

p = 0x83f39daf527c6cf6360999dc47c4f0944ca1a67858a11bd915ee337f8897f36eff98355d7c35c2accdf4555b03a9552b4bf400915320ccd0ba60b0cb7fcad723
g = 0x15a5f7dec38869e064dd933e23c64f785492854fbe8a6e919d991472ec68edf035eef8c15660d1f059ca1600ee99c7f91a760817d7a3619a3e93dd0162f7474bbf


def test():
    for _ in range(10):
        x = random.randint(1, p)
        n = random.randint(1, 20)
        m = p**n
        assert pow(g, x, m) == fast_exp(x, n)

def chall():
    n = 1000
    x = random.randint(1, p**(n-1))
    y = fast_exp(x, n)
    return x, y


def stop(signum, stack):
    print("Too slow")
    exit(1)


def main():
    x, y = chall()
    timeout = 60
    print(hex(y))
    print("Now gimme x")
    signal.alarm(timeout)
    x_inp = int(input(), 16)
    if x == x_inp:
        print("Wow, impressive!")
        print(flag)
    else:
        print("Nope, sorry")


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, stop)
    #test()
    main()
