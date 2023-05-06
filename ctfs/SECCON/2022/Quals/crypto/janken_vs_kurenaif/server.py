import os
import signal
import random
import secrets

FLAG = os.getenv("FLAG", "fake{cast a special spell}")


def janken(a, b):
    return (a - b + 3) % 3


signal.alarm(1000)
print("kurenaif: Hi, I'm a crypto witch. Let's a spell battle with me.")

witch_spell = secrets.token_hex(16)
witch_rand = random.Random()
witch_rand.seed(int(witch_spell, 16))
print(f"kurenaif: My spell is {witch_spell}. What about your spell?")

your_spell = input("your spell: ")
your_random = random.Random()
your_random.seed(int(your_spell, 16))

for _ in range(666):
    witch_hand = witch_rand.randint(0, 2)
    your_hand = your_random.randint(0, 2)

    if janken(your_hand, witch_hand) != 1:
        print("kurenaif: Could you come here the day before yesterday?")
        quit()

print("kurenaif: Amazing! Your spell is very powerful!!")
print(f"kurenaif: OK. The flag is here. {FLAG}")
