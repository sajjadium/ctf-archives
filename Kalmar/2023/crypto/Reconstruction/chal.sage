import random

rng = random.SystemRandom()

num_parties = 1000
threshold = int(0.1111 * num_parties)
num_compromised = int(0.37 * num_parties)

prime = (2**384).next_prime()
F = GF(prime)

class Party:
    def __init__(self, share):
        self.share = share
        self.compromised = False

    def compromise(self):
        self.compromised = True

    def get_share(self):
        if self.compromised:
            return self.share
        else:
            return F(rng.randrange(F.order()))

def share(secret):
    R.<x> = F['x']

    poly = secret * x**threshold
    for i in range(threshold):
        poly += x**i * F(rng.randrange(F.order()))

    return [Party(poly(F(j))) for j in range(num_parties)]

def main():
    with open('flag.txt', 'r') as f:
        flag = f.read().strip()
    assert(len(flag) < prime.nbits()*8)

    # Share the secret.
    secret = F(int.from_bytes(flag.encode(), 'little'))
    parties = share(secret)

    # Oops, the adversary has compromised some of the parties!
    for i in rng.sample(range(num_parties), num_compromised):
        parties[i].compromise()

    # The adversary is requesting the shares! All is lost!
    for s in parties:
        print(s.get_share())

if __name__ == "__main__":
    main()
