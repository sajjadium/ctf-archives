import random

# user version
def input_lines():
    lines = []
    print("Welcome to the squ1rrel lottery! 9 winning numbers will be selected, and if any of your tickets share 3 numbers with the winning ticket you'll win! Win 1000 times in a row to win a flag")
    for i in range(1, 41):
        while True:
            line = input(f"Ticket {i}: ").strip()
            numbers = line.split()
            if len(numbers) != 9:
                print("Please enter 9 numbers")
                continue
            try:
                numbers = [int(num) for num in numbers]
                if not all(1 <= num <= 60 for num in numbers):
                    print("Numbers must be between 1 and 60")
                    continue
                lines.append(set(numbers))
                break
            except ValueError:
                print("Please enter only integers.")
    return lines


user_tickets = input_lines()
wincount = 0
for j in range(1000):
    winning_ticket = random.sample(range(1, 61), 9)

    win = False
    for i in user_tickets:
        if len(i.intersection(set(winning_ticket))) >= 3:
            print(f'Win {j}!')
            win = True
            wincount += 1
            break
    if not win:
        print("99 percent of gamblers quit just before they hit it big")
        break

if wincount == 1000:
    print("squ1rrelctf{test_flag}")
