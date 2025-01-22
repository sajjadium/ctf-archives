import random
from flag import FLAG

def genRandMath():
    eqn = f'{random.randint(-1000, 1000)}'
    eqn = f"{eqn} {random.choice(['+', '*', '-', '//'])} {random.randint(-1000, 1000)}"
    while random.randint(0, 3) != 1:
        eqn = f"{eqn} {random.choice(['+', '*', '-', '//'])} {random.randint(-1000, 1000)}"
    try:
        res = eval(eqn)
        return eqn, res
    except ZeroDivisionError:
        return genRandMath()

print("Welcome to a simple math test.")
print("If you solve these basic math questions, I will give you the flag.")
print("Good Luck")

for i in range(1000):
    eqn, correct = genRandMath()
    print(f"Question: {eqn}")
    res = int(input("Answer: "))
    if res != correct:
        print(f"Wrong!! Correct answer is {correct}")
        exit()
    
    print(f"Correct {i+1}/1000")

print(f"Congratz! Here is the flag {FLAG}")
    