from Crypto.Util.number import bytes_to_long, getPrime, isPrime
from sage.all import matrix, Zmod
from flag import flag


def nextPrime(prim):
    if isPrime(prim):
        return prim
    else:
        return nextPrime(prim+1)

p1 = getPrime(128)
p2 = nextPrime(p1 * 1)
p3 = nextPrime(p2 * 3)
p4 = nextPrime(p3 * 3)
p5 = nextPrime(p4 * 7)

primes = [p1, p2, p3, p4, p5]

n = p1 * p2 * p3 * p4 * p5

fragments = [bytes_to_long(flag[5*i:5*i+5]) for i in range(25)]

e = 31337

topG = matrix(Zmod(n), [[fragments[5*i + j] for j in range(5)] for i in range(5)])
bottomG = topG ** e

with open("output.txt", "w") as file:
    file.write(f"n = {n}\n\n")
    file.write("Ciphertext Matrix:\n\n")
    for row in bottomG:
        for num in row:
            file.write(str(num) + " ")
        file.write("\n\n")

