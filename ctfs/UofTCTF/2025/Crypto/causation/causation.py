import secrets

MASK = (1<<64)-1

def rotl(x, k):
    return ((x<<k)&MASK)|(x>>(64-k))

class PRNG():
    def __init__(self, state):
        self.p = 0
        assert not all(i==0 for i in state)
        assert len(state)==16
        assert all(i<(1<<64) for i in state)
        self.state = state
    def next(self):
        q = self.p
        self.p = (self.p+1)&15
        s0 = self.state[self.p]
        s15 = self.state[q]
        res = (rotl(s0+s15, 23)+s15)&MASK
        s15^=s0
        self.state[q] = (rotl(s0, 25)^s15^(s15<<27))&MASK
        self.state[self.p] = rotl(s15, 36)
        return int(11*res/(2**64))

seed = [secrets.randbits(64) for i in range(16)]
salt = [secrets.randbits(64) for i in range(16)]
seed2 = [i^j for i,j in zip(seed, salt)]

print("Salt: ", salt)

rng1 = PRNG(seed)
rng2 = PRNG(seed2)

print("You now need to guess at least 20 out of 50 values correctly, good luck!")
print("Please input 50 points in the call sequence")
points = list(map(int, input().split()))
points.sort()
assert len(points)==50 and len(set(points))==50
assert points[0]>=0
assert points[-1]<100000

correct = 0
incorrect = 0
i = 0
while len(points)>0:
    if i==points[0]:
        print(rng1.next())
        print("What's your guess?")
        guess = int(input())
        if guess==rng2.next():
            correct+=1
        else:
            incorrect+=1
        points = points[1:]
    else:
        rng1.next()
        rng2.next()
    i+=1
print("You achieved a score of", correct)
if correct>=20:
    print(open("flag.txt").read())
