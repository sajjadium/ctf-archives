from dataclasses import dataclass
from cmath import exp
import secrets
import time
import os

FLAG = os.getenv("FLAG") or "test{flag_for_local_testing}"


@dataclass
class Wave:
    a: int
    b: int

    def eval(self, x):
        theta = x / self.a + self.b
        return ((exp(1j * theta) - exp(-1j * theta)) / 2j).real

ALL_WAVES = [Wave(a, b) for a in range(2, 32) for b in range(7)]

class MaximTwister:
    """
    Next-generation PRNG with really **complex** nature.
    More reliable than /dev/random cuz doesn't block ever.
    """

    def __init__(self, state=None):
        if state is None:
            state = (1337, [secrets.randbits(1) for _ in ALL_WAVES])

        self.point = state[0]
        self.waves = [wave for wave, mask in zip(ALL_WAVES, state[1]) if mask]

    def get_randbit(self) -> int:
        result = 0
        for wave in self.waves:
            # you would never decompose a sum of waves 😈
            result += round(wave.eval(self.point))
        # especially if you know only the remainder, right? give up
        result %= 2
        self.point += 1

        return result

    def get_randbits(self, k: int) -> int:
        return int("".join(str(self.get_randbit()) for _ in range(k)), 2)

    def get_token_bytes(self, k: int) -> bytes:
        return bytes([self.get_randbits(8) for _ in range(k)])


print("*** BUG DESTROYER ***")
print("You encounter: 😈 SEGMENTATION FAULT 😈")
opponent_hp = int(time.time()) * 123
days_passed = 0

random = MaximTwister()

while True:
    print(
        f"🕺 You ({10-days_passed} days till release) -- 😈 SEGMENTATION FAULT ({opponent_hp} lines)"
    )
    print(f"Day {days_passed + 1}. You can:")
    print("1. Make a fix")
    print("2. Call a senior")
    choice = input("> ").strip()
    if choice == "1":
        damage = random.get_randbits(32)
        opponent_hp -= damage
        if opponent_hp <= 0:
            print(
                f"You commited a fix deleting {damage} lines. Miraculously, it worked!"
            )
            break
        else:
            print(f"You commited a fix deleting {damage} lines. The bug remained 😿")
    elif choice == "2":
        print("You called a senior. It's super effective! The bug is destroyed.")
        break
    else:
        print(
            f"You spent {random.get_randbits(4)} hours doing whatever {choice} means."
        )

    print("A day has passed. You couldn't fix the bug.")
    days_passed += 1

    if days_passed == 10:
        print("It's release date! The bug is still there. You're fired.")
        exit()

print("The bug is gone! You got a raise.")
print(
    "In your new office you see a strange door. It is locked. You try to guess the password from the digital lock:"
)
password = input("> ")
if bytes.fromhex(password) == random.get_token_bytes(16):
    print("Somehow, you guessed the password! The room opens before you.")
    print("You see a mysterious text:", FLAG)
    print(
        "What could it mean?... You turn around and see your boss right behind you..."
    )
    print("BAD ENDING")
else:
    print("Incorrect. Well, let's get back to work...")
    print("GOOD ENDING")
