import os
import signal
from random import SystemRandom
from Crypto.Util.number import isPrime, bytes_to_long
random = SystemRandom()
def challenge():
    signal.alarm(30)
    salt = bytes_to_long(os.urandom(20)) | 1
    print(f"{salt = }")
    P = int(input("P: "))
    assert P.bit_length() >= 4096 # Nist recommended
    assert P.bit_length() <= 16384 # I don't like big food
    assert P % 2**160 == salt
    assert isPrime(P)
    g = random.randint(0, P-1)
    x = random.randint(0, P-2)
    public = pow(g, x, P)
    print(f"{g = }")
    print(f"{public = }")
    if pow(g, int(input("x: ")), P) == public:
        print("Flag:", os.getenv("FLAG", "ISITDTU{dark_dark_bruh_bruh_lmao_test_flag}"))
def timeout_handler(sig, frame):
    print('Time out!')
    exit(0)
if __name__ == "__main__":
    if os.system("python3 PoW.py") != 0:
        exit(1)
    signal.signal(signal.SIGALRM, timeout_handler)
    try:
        challenge()
    except:
        pass
    finally:
        print("Bye")