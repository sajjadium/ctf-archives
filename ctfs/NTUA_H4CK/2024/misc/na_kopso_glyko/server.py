import random
import json
from secret import FLAG

def random_flouri_generator():
    m = 10**30
    return random.randint(1, m)**11 + 17*random.randint(1, m)**7 - 42*random.randint(1, m)**5 + 1337*random.randint(1, m)*3 + 31337*random.randint(1, m)

def check_password(password, your_guess):
    for i in range(len(password)):
        if FLAG[i] != password[i]: 
            # password is incorrect, but let's see if you win the flouri

            for _ in range(10000):
                if your_guess == random_flouri_generator():
                    print(f"You're sweet AND lucky, here you go: {FLAG}")
                    return True
            return False
    if len(FLAG) == len(password):
        return True
    return False

print("NA KOPSO GLYKO???")
print("Sweetie, tell me my password if you want dessert. Or guess my number, I'll give you 10000 chances because you're my favorite grandchild.")
while True:
    try:
        inp = json.loads(input("Give me password and number in json: "))
        password = inp["password"]
        guess = int(inp["number"])
    except:
        print("Something wrong honey?")
        break
    if check_password(password, guess):
        print("GLYKO and HUGS")
        break
    else:
        print("It's ok honey, you'll get it next time")