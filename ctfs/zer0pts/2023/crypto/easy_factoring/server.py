import os
import signal
from Crypto.Util.number import *

flag = os.environb.get(b"FLAG", b"dummmmy{test_test_test}")

def main():
    p = getPrime(128)
    q = getPrime(128)
    n = p * q

    N = pow(p, 2) + pow(q, 2)

    print("Let's factoring !")
    print("N:", N)

    p = int(input("p: "))
    q = int(input("q: "))

    if isPrime(p) and isPrime(q) and n == p * q:
        print("yey!")
        print("Here you are")
        print(flag)
    else:
        print("omg")

def timeout(signum, frame):
    print("Timed out...")
    signal.alarm(0)
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(30)
    main()
    signal.alarm(0)
