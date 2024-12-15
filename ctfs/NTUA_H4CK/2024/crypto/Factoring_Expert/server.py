import random
from Crypto.Util.number import isPrime
from secret import FLAG

e = 65537
NUMROUNDS = 7

def get_primes_and_messages(nbits):
    primes = []
    messages = []
    ind = 0
    while True:
        num = random.randint(0, 2**nbits - 2)
        poss_prime = int(f"{(1 << nbits) + num}{ind:04}")
        if isPrime(poss_prime):
            primes.append(poss_prime)
        else:
            messages.append(int(f"{num}{ind:04}"))
        if len(primes) == 2:
            return primes, messages
        ind += 1

print("Welcome to the Advanced Factoring Challenge")
print(f"Pass {NUMROUNDS} rounds of tests, and you'll have proven your worth")

for i in range(1, 1 + NUMROUNDS):
    print(f"Round {i}")
    difficulty = 32*i
    primes, msgs = get_primes_and_messages(difficulty)
    p, q = primes
    n = p*q
    print(f"{n = }")
    print("Messages:", [pow(msg, e, n) for msg in msgs])
    for msg in msgs:
        try:
            answer = int(input())
        except:
            print("something went wrong")
            exit()
        if answer != msg:
            print("Nope")
            exit()

print(FLAG)