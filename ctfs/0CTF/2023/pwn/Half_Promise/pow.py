import random, sys
import gmpy2

def proof_of_work(sec = 60):
    # From 0CTF/TCTF 2021
    p = gmpy2.next_prime(random.getrandbits(512))
    q = gmpy2.next_prime(random.getrandbits(512))
    n = p*q
    c = 2900000
    t = c*sec + random.randint(0,c)
    print('Show me your computation:')
    print(f'2^(2^{t}) mod {n} = ?')
    print('Your answer: ', end='')
    try:
        sol = int(sys.stdin.readline())
        phi = (p-1)*(q-1)
        u = pow(2, t, phi)
        w = pow(2, u, n)
        if w == sol:
            print('Correct!')
            return True
        else:
            print('Wrong Answer!')
            exit(1)
    except ValueError:
        print('Invalid Input!')
        exit(1)

if __name__ == '__main__':
    if proof_of_work():
        exit(0)
    else:
        exit(1)
