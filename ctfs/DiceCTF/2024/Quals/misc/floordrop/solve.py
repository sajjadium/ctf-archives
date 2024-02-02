import sys
import gmpy2

MODULUS = 2**44497-1

def sloth_root(x, p):
    exponent = (p + 1) // 4
    x = gmpy2.powmod(x, exponent, p)
    return int(x)

def solve_challenge(x):
    y = sloth_root(x, MODULUS)
    return y

def main():
    chal = int(sys.argv[1])
    sol = solve_challenge(chal)
    print(sol.to_bytes((sol.bit_length() + 7) // 8, 'big').hex())

if __name__ == '__main__':
    main()