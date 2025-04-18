from math import gcd

def is_prime(n):
    if n == 2: 
        return True
    if n == 1 or n & 1 == 0: 
        return False
    d = n - 1
    while d & 1 == 0:
        d >>= 1
    for a in range(500):
        if gcd(a, n) != 1:
            continue
        t = d
        y = pow(a, t, n)
        while t != n - 1 and y != 1 and y != n - 1:
            y = (y * y) % n
            t <<= 1
        if y != n - 1 and t & 1 == 0:
            return False
    return True

if __name__ == '__main__':
    n = int(input("What is your favorite prime number?: "))
    if n <= 2 or 4096 <= n.bit_length():
        print("Hmm... I don't like this.")
        exit(0)
    if not is_prime(n):
        print(":(")
        exit(0)
    x = int(input("What is your favorite number?: "))
    if x <= 1 or x >= n - 1:
        print(":(")
        exit(0)
    if pow(x, 2, n) == x:
        print("Wow! How did you do that?")
        with open("flag.txt") as f:
            print(f.read())
    else:
        print("Nice!")
    exit(0)
