from subprocess import Popen, PIPE, DEVNULL
from Crypto.Util.number import getPrime
from secret import fname, flag
import time, string, secrets, os

def keygen():
    pr = Popen(['python3', '-i'], stdin=PIPE, stdout=DEVNULL, stderr=DEVNULL, text=True, bufsize=1)

    p, q = getPrime(1024), getPrime(1024)
    N, e = p * q, 0x10001
    m = secrets.randbelow(N)
    c = pow(m, e, N)

    pr.stdin.write(f"{(N, p, c) = }\n")
    pr.stdin.write(f"X = lambda m: open('{fname}', 'w').write(str(m))\n")
    # X marks the spot!
    
    return pr, m

def verify(pr, m, msg):
    time.sleep(1)

    assert int(open(fname, 'r').read()) == m
    os.remove(fname)
    pr.kill()

    print(msg)

# Example!
pr, m = keygen()
example = [
    "q = N // p",
    "phi = (p - 1) * (q - 1)",
    "d = pow(0x10001, -1, phi)",
    "m = pow(c, d, N)",
    "X(m)"
]

for code in example:
    pr.stdin.write(code + '\n')

verify(pr, m, "I showed you how RSA works, try yourself!")


# Your turn!
pr, m = keygen()
while code := input(">>> "):
    if (len(code) > 3) or any(c == "\\" or c not in string.printable for c in code):
        print('No hack :(')
        continue
    pr.stdin.write(code + '\n')

verify(pr, m, flag)
