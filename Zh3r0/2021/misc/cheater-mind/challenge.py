from random import randint, random
from collections import Counter

class Agent:
    def __init__(self,N,K,mutation,guess_limit):
        self.N = N
        self.K = K
        self.mutation = mutation
        self.guess_limit = guess_limit
        self.secret = [randint(1,N) for i in range(K)]

    def play(self,guess):
        if guess==self.secret:
            return self.K,0
        mutated = [i if random() > self.mutation 
                   else randint(1,self.N) for i in self.secret]
        bulls = sum(a==b for a,b in zip(mutated,guess))
        cows = Counter(mutated)&Counter(guess)
        return bulls, sum(cows.values())-bulls

    def game(self):
        try:
            for guess_no in range(self.guess_limit):
                guess = list(map(int,input('enter your guess as space separated integers:\n').strip().split()))
                bulls,cows = self.play(guess)
                print(bulls,cows)
                if bulls == self.K:
                    return True
            return False
        except:
            print("Error, exiting")
            exit(1)

LEVELS = [ #N,K,mutation,guess_limit
    [6,6,0,7],
    [8,6,0,8],
    [8,8,0,9],
    [6,6,0.05,10],
    [8,6,0.05,11],
    [6,6,0.1,12],
]

print("""Can you beat me at mastermind when I am not so honest?
      https://en.wikipedia.org/wiki/Mastermind_(board_game)""")

for level,(N,K,mutation,guess_limit) in enumerate(LEVELS,start=1):
    print("Level {}, N={}, K={}, mutation={}, guess limit={}".format(
        level,N,K,mutation,guess_limit))
    if Agent(N,K,mutation,guess_limit).game():
        print('level passed, good job')
    else:
        print('You noob, try again')
        exit(1)


from secret import flag
print('you earned it :',flag)
