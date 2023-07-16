#!/usr/local/bin/python
from flag import flag
import random


def my_very_cool_function(x):
    return pow(x, 2141, 998244353)


successes = 0
prefixes = ["1", "4", "1", "2"]
suffixes = ["0533", "0708", "1133"]  # skittles1412 birthday Orz... May has 30 days ofc (he claims 12/03 but i call cap)


def gen_goal():
    goal = random.choice(prefixes)
    for i in range(140):
        while (x := random.choice(prefixes)) == goal[-1] and random.randint(1, 5) != 1:
            pass
        goal += x
    goal += random.choice(suffixes)
    return int(goal)


def run_testcase():
    goal = gen_goal()
    print(f"Goal: {goal}")

    whiteboard = {my_very_cool_function(167289653), my_very_cool_function(68041722)}  # stO HBD BRYAN GAO Orz
    print(whiteboard)

    for _ in range(1412):
        try:
            a, b = map(int, input("Numbers to combine? ").split())
            assert a in whiteboard and b in whiteboard

            x = 2 * a - b
            whiteboard.add(x)

            if x == goal:
                print("Good job")
                return True

        except:
            print("smh bad input *die*")
            exit("Exiting...")

    return False


for i in range(5):
    ok = run_testcase()
    assert ok

print("happy birthday to you too!")
print(flag)
