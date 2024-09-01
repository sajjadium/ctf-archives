import quantum, random

N = 500


def bye():
    print("bitset")
    exit(0)


def main():
    a = quantum.gen(N - N // 10, N)
    n = len(a)
    print(n)

    print("Ask me anything?")
    q = 0
    while True:
        m = int(input().strip())

        if m == -1:
            break

        q += m
        if q > 1.9 * n:
            bye()

        xs = list(map(int, input().split()))
        ys = list(map(int, input().split()))

        if len(xs) != m or len(ys) != m:
            bye()

        resp = []
        for x, y in zip(xs, ys):
            if 0 > x or x >= n or 0 > y or y >= n:
                bye()
            resp.append(quantum.ask(x, y))

        print(" ".join([str(x) for x in resp]))

    print("It is easy to prove that you can answer the following queries!")
    q = random.randint(N - N // 10, N)
    print(q)

    expected = [0] * q
    for i in range(q):
        x0 = random.randint(1, n - 1)
        x1 = random.randint(x0, n - 1)
        y0 = random.randint(1, n - 1)
        y1 = random.randint(y0, n - 1)
        expected[i] = quantum.query(x0, y0, x1, y1)
        print(x0, y0, x1, y1)

    output = list(map(int, input("Your answer? ").split()))
    if output == expected:
        print("AC")
    else:
        bye()

    print("aeren orz", quantum.FLAG)


if __name__ == "__main__":
    try:
        main()
    except:
        bye()
