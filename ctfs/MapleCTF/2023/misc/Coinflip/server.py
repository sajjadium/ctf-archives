from random import Random
from secret import FLAG
import signal

class Coin:
    def __init__(self, coin_id):
        self.random = Random(coin_id)
        self.flips_left = 0
        self.buffer = None

    def flip(self):
        if self.flips_left == 0:
            self.buffer = self.random.getrandbits(32)
            self.flips_left = 32
        res = self.buffer & 1
        self.buffer >>= 1
        self.flips_left -= 1
        return res

if __name__ == "__main__":
    signal.alarm(60)
    print("Welcome to Maple Betting!")
    print("We'll be betting on the outcome of a fair coin flip.")
    print("You'll start with $1 - try to make lots of money and you'll get flags!")

    game_id = input("Which coin would you like to use? ")
    num_rounds = input("How many rounds do you want to go for? ")
    num_rounds = int(num_rounds)
    if num_rounds > 20_000_000:
        print("Can't play that long, I'm afraid.")
        exit(1)

    print("Alright, let's go!")
    coin = Coin(int(game_id, 0))
    money = 1
    for nr in range(num_rounds):
        money += [1, -1][coin.flip()]
        if money <= 0:
            print(f"Oops, you went broke at round {nr+1}!")
            exit(1)

    print(f"You finished with ${money} in the pot.")
    if money < 18_000:
        print("At least you didn't go broke!")
    elif money < 7_000_000:
        print(f"Pretty good!")
    else:
        print(f"What the hell?! You bankrupted the casino! Take your spoils: {FLAG}")
