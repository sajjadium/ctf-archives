import random
import os

FLAG = os.getenv("FLAG", "ping{FAKE}")

random.seed(random.randint(0, 10_000_000))

opponent_balance = 10_000_000
user_balance = 50
round_num = 1


def print_balance():
    print(f"{user_balance=}")
    print(f"{opponent_balance=}")


def spacer():
    print("-" * 64)


def roll(n: int):
    return random.randint(1, n)


def roll_number(n: int, user: str = "user"):
    if user == "user":
        user = "opponent"
    else:
        user = "user"

    if n == 1:
        return user
    else:
        number = roll(n)
        print(f"{user} rolls {number}")
        return roll_number(number, user)


def round():
    global user_balance, opponent_balance
    if user_balance > 10_000_000:
        print(f"{FLAG=}")
        exit(0)
    print_balance()
    spacer()
    bet = int(input("How much do you want to bet? "))
    if bet > user_balance:
        print("You don't have enough money!")
        return
    if bet <= 0 or bet > opponent_balance:
        print("Invalid amound of money")
        return

    user_balance -= bet
    opponent_balance -= bet
    winnings = bet + bet
    winner = roll_number(100)
    if winner == "user":
        print("You won!")
        user_balance += winnings
    else:
        print("You lost!")
        opponent_balance += winnings


def main():
    print("welcome to the death roll!")
    print(
        "it is a game that is common in WoW game on chat to risk or double your gold!"
    )
    print("short example on how it works:")
    spacer()
    print("you have 50 gold")
    print("you can bet 1-50 gold")
    print("First roll is random number from 1 to 100")
    print("when you roll 47 then the opponent rolls from 1 to 47")
    print("when opponent roll 20 then you roll from 1 to 20")
    print("the person who gets to roll 1 loses the money")

    start = input("Do you want to start? (y/n): ")
    while start != "n" and start != "y":
        start = input("Do you want to start? (y/n): ")
    if start == "n":
        exit(0)
    while True:
        round()


if __name__ == "__main__":
    main()
