#!/usr/local/bin/python

import os

balances = [10, 20, 50, 16, 29, 52, 100000]

PERMS_ADMIN = {
    "MAX_INDEX": len(balances) - 1
}

PERMS_AGENT = {
    "MAX_INDEX": len(balances) - 2
}

def main():
    perms = PERMS_AGENT
    wallet = 0
    idx = int(input("Which account would you like to withdraw from? "))
    if idx > perms["MAX_INDEX"]:
        print("Unauthorized")
        return
    wallet += balances[idx]
    balances[idx] = 0

    print(f"You now have ${wallet} in your wallet.\n")

    if wallet >= 100000:
        print("Thanks for storing a lot of $$ at our bank.")
        print("You qualify for free wealth management services.")
        print(f"To access this service, please email {os.getenv('FLAG')}@bxmctf.bank.\n")

    print("Thank you for banking with BxMCTF Bank.")


if __name__ == "__main__":
  main()
