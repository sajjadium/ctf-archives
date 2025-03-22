from secret import flag1, flag2, flag3, flag4, SHRIMPVALS
import random

SHRIMPS = {
    SHRIMPVALS[0]: flag1,
    SHRIMPVALS[1]: flag2,
    SHRIMPVALS[2]: flag3,
    SHRIMPVALS[3]: flag4,
}

def whitelist(shrimp: str) -> bool:
    if any([c not in "<([+-~*])>" for c in shrimp]) or len(shrimp) > 210:
        return False
    return True

if __name__ == "__main__":
    for shrimpval in SHRIMPS:
        assert type(shrimpval) == int
        assert type(SHRIMPS[shrimpval]) == str
        assert len(SHRIMPS[shrimpval]) > 100000

    try:
        while len(SHRIMPS) > 0:
            shrimp = input("so youre telling me: ")

            if not whitelist(shrimp):
                print("youve gotta be squidding me")
                exit(1)

            shrimp = eval(shrimp, {'__builtins__': None})

            if type(shrimp) != int:
                print("its become a prawnblem")
                exit(1)

            found = False
            for shrimpval in SHRIMPS:
                if shrimpval == shrimp:
                    print("it doesnt get any betta than this:", SHRIMPS[shrimpval])
                    found = True
                    SHRIMPS.pop(shrimpval)
                    break
                elif abs(shrimpval - shrimp) < 10:
                    print("i was just squidding")
                    found = True
                    SHRIMPS.pop(shrimpval)
                    break
                elif abs(shrimpval - shrimp) < 20:
                    print("i highly trout that")
                    found = True
                    SHRIMPS.pop(shrimpval)
                    break

            if not found:
                print(f"weve come to a shrimpasse ({random.choice(SHRIMPVALS)*random.choice(SHRIMPVALS)})")

    except Exception as e:
        print("it took a tuna for the worse")
        exit(1)