from inputimeout import inputimeout, TimeoutOccurred
import random, sys

with open('flag.txt') as f:
	flag = f.read()

def main():
	print("Here is how the lottery works:")
	print("- Players purchase tickets comprising their choices of six different numbers between 1 and 70")
	print("- During the draw, six balls are randomly selected without replacement from a set numbered from 1 to 70")
	print("- A prize is awarded to any player who matches at least two of the six drawn numbers.")
	print("- More matches = higher prize!")
	while True:
		print("\n********************\nHow many tickets would you like to buy? There is a limit of 50 tickets per person")
		try:
			reply = int(inputimeout(prompt='>> ', timeout=60))
		except ValueError:
			reply = 0
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()
		if reply > 50 or reply < 1:
			print("That is an invalid choice!\n")
		else:
			break
	tickets = []
	for x in range(reply):
		ticket = []
		print(f"\n********************\nPlease give the numbers for ticket {x+1}:")
		for _ in range(6):
			while True:
				try:
					number = int(inputimeout(prompt='>> ', timeout=60))
				except TimeoutOccurred:
					print("Oof! Not fast enough!\n")
					sys.exit()
				except ValueError:
					number = 0
				if number > 70 or number < 1:
					print("That is an invalid choice!\n")
				else:
					break
			ticket.append(number)
		tickets.append(ticket)
	winnings = [0, 0, 1, 100, 1000, 100000, 10000000]
	print(f"\n********************\nLet's see if you can win in {10**6} consecutive rounds of the lottery and make a profit at the end of it!")
	profit = 0
	for i in range(10**6):
		draw = set([])
		while len(draw) != 6:
			draw.add(random.randint(1,70))
		won_prize = False
		for ticket in tickets:
			profit -= 1
			matches = len(draw.intersection(set(ticket)))
			if matches > 1:
				won_prize = True
			profit += winnings[matches]
		if won_prize:
			if (i+1)%(10**5) == 0:
				print(f"You made it through {i+1} rounds! Profit so far is ${profit}")
		else:
			print(f"Draw {i+i}: {draw}, profit: ${profit}")
			print(f"\n********************\nAh shucks! Look's like you did not win any prizes this round. Better luck next time")
			sys.exit()
	if profit > 0:
		print(f"\n********************\nWow! You broke the lottery system! Here's the well-deserved flag --> {flag}")

if __name__ == "__main__":
	main()