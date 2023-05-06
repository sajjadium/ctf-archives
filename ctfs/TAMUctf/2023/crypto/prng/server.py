import secrets
from flag import flag, m, a, c

class Rand:
    def __init__(self, seed):
        self.m = m
        self.a = a
        self.c = c
        self.seed = seed
        if seed % 2 == 0: # initial state must be odd
            self.seed += 1

    def rand(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

def main():
    seed = secrets.choice(range(0, 0x7fffffffffffffff))
    rng = Rand(seed)
    
    chall = []
    for _ in range(10):
        chall.append(rng.rand())

    print(f"Authenticate. Provide the next 10 numbers following")
    for c in chall:
        print(c)

    for _ in range(10):
        x = int(input('> '))
        if x != rng.rand():
            print("Access denied.")
            exit()
    
    print("Access granted.")
    print(flag)


if __name__ == "__main__":
    main()
