import random, time

def solve(eggs):
    redactedscript = """
    █ █ █████████
    ██ █ ██

    ███ █ ██ █████████
        ██████████████ █ ██

    ████████ █ ██████████

    ███ █ ██ █████████
        ███ █ ██ █████████
            ██ █ ██ █ ███ █ ██ ██
                ████████

            ██ █ ██ ██
                ████████ █ ████ █ █████
            ██ █ ██ ██
                ████████ █ █████████████ ███████ █ ███

            ████████ ██ ██████████

    ██████ ██████████
    """

    return sum([ord(c) for c in redactedscript])

n = 1000

start = time.time()

for _ in range(10):
    eggs = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(random.randint(0, 696969))
            print(row[j], end=' ')
        eggs.append(row)
        print()

    solution = solve(eggs)
    print("optimal: " + str(solution) + " 🥚")
    inputPath = input()
    inputAns = eggs[0][0]
    x = 0
    y = 0

    for direction in inputPath:
        match direction:
            case 'd':
                x += 1
            case 'r':
                y += 1
            case _:
                print("🤔")
                exit()

        if x == n or y == n:
            print("out of bounds")
            exit()

        inputAns += eggs[x][y]



    if inputAns < solution:
        print(inputAns)
        print("you didn't find enough 🥚")
        exit()
    elif len(inputPath) < 2 * n - 2:
        print("noooooooooooooooo, I'm still in Brazil")
        exit()

    if int(time.time()) - start > 60:
        print("you ran out of time")
        exit()

print("tnxs for finding all my 🥚")
f = open("/flag.txt", "r")
print(f.read())
