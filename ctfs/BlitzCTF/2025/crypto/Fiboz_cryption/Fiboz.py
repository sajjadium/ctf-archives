import sys


def x7a3(n):
    s = 0
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        s += 1
    return s


def y4f2(l, a=1, b=1):
    r = [a, b]
    for _ in range(l - 2):
        r.append(r[-1] + r[-2])
    return r


def z9k1(s, k):
    return bytes(ord(c) ^ (k[i % len(k)] % 256) for i, c in enumerate(s))


def main():
    print("Challenge ready!")
    try:
        l = int(input("Enter length: "))
        a = int(input("First seed [1]: ") or 1)
        b = int(input("Second seed [1]: ") or 1)
    except:
        print("Error")
        sys.exit(1)

    f = y4f2(l, a, b)
    c = [x7a3(n) for n in f]
    t = input("\nInput text: ")
    if not t:
        t = "flag{example_flag}"

    e = z9k1(t, c)
    with open('output.enc', 'wb') as file:
        file.write(e)
    print("Output written to output.enc (hex format)")


if __name__ == "__main__":
    main()