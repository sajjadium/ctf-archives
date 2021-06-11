#!/usr/bin/python
from itertools import product
from random import randint
import sys
from hashlib import sha256
import pickle
import base64

def check_winner(board):
	positions_groups = (
	    [[(x, y) for y in range(3)] for x in range(3)] + # horizontals
	    [[(x, y) for x in range(3)] for y in range(3)] + # verticals
	    [[(d, d) for d in range(3)]] + # diagonal from top-left to bottom-right
	    [[(2-d, d) for d in range(3)]] # diagonal from top-right to bottom-left
	)
	for pos in positions_groups:
		line = [board[a][b] for (a,b) in pos]
		if len(set(line)) == 1 and line[0] != "_":
			if line[0] == "X":
				return "X"
			else:
				return "O"
	return "_"

class Game():
	def __init__(self):
		self.board = [["_" for a in range(3)] for b in range(3)]
		pass


	def clear(self):
		print("\033c", end="")

	def print_board(self):
		print(f"╔═══╦═══╦═══╗")
		print(f"║ {self.board[0][0]} ║ {self.board[0][1]} ║ {self.board[0][2]} ║")
		print(f"╠═══╬═══╬═══╣")
		print(f"║ {self.board[1][0]} ║ {self.board[1][1]} ║ {self.board[1][2]} ║")
		print(f"╠═══╬═══╬═══╣")
		print(f"║ {self.board[2][0]} ║ {self.board[2][1]} ║ {self.board[2][2]} ║")
		print(f"╚═══╩═══╩═══╝")

	def check_winner(self):
		winner = check_winner(self.board)
		if winner == "X":
			return (False, winner)
		elif winner == "O":
			print("The computer won :(")
			return (False, winner)
		if all(self.board[a][b] != "_" for a, b in product(range(3),repeat=2)):
			print("No moves left...")
			return (False, "_")
		return (True, "_")


def play_game():
	game = Game()
	def player_turn():
		game.clear()
		game.print_board()
		print("Enter move (0-indexed, row col): ")
		while True:
			loc = input("> ").split(" ")
			if len(loc) != 2:
				print("invalid format")
				continue
			try:
				row, col = (int(loc[0]), int(loc[1]))
				if col > 2 or row > 2:
					print("move out of bounds")
					continue
				if game.board[row][col] != "_":
					print("that space is already full!")
					continue
				game.board[row][col] = "X"
				break
			except ValueError:
				print("invalid integer literal")
				continue

		game.clear()
		game.print_board()
		cont, winner = game.check_winner()
		return cont

	def ai_turn():
		cont, winner = game.check_winner()
		while True:
			row, col = (randint(0,2), randint(0,2))
			if game.board[row][col] == "_":
				break
		game.board[row][col] = "O"
		cont, winner = game.check_winner()
		return cont


	while player_turn() and ai_turn():
		pass

	return "X" == check_winner(game.board)

TARGET_NO = 133713371337
wins = 0

f = open("flag.txt","r")
flag = f.read()
f.close()


def menu():
	print(f"Welcome to my new game!  I bet you can't beat me {TARGET_NO} times!!  You've won {wins} times. ")
	print("1. Play game")
	print("2. Redeem prize")
	print("3. Save progress")
	print("4. Load progress")
	print("5. Check stats")

def get_hash(w):
	m = sha256()
	m.update((str(wins) + flag).encode())
	return base64.b64encode(m.digest()).decode()

menu()

while True:
	selection = input("> ")

	if selection == "1":
		if play_game():
			wins += 1
		menu()
	elif selection == "2":
		if wins >= TARGET_NO:
			print(f"Great job!  You definitely deserve this: {flag}")
			f.close()
			sys.exit()
		else:
			print(f"You don't have enough wins... you need {TARGET_NO-wins} more")
		pass
	elif selection == "3":

		data = {"wins": wins, "security": get_hash(wins)}
		print(f"Here you go!  Come back and try again! \"{base64.b64encode(pickle.dumps(data)).decode()}\"")
		pass
	elif selection == "4":
		save = input("What was the code I gave you last time? ")
		data = pickle.loads(base64.b64decode(save))

		if get_hash(data['wins']) != data['security']:
			print("Hey, the secret code I left isn't correct.  You aren't trying to cheat are you :/")
			continue
		else:
			wins = data['wins']
			print(f"Okay, that all checks out!  I'll mark you down as {wins} wins")
		pass
	elif selection == "5":
		print(f"You've won {wins} times, so you need {TARGET_NO-wins} more")
	else:
		print("That doesn't look like an option...")
		continue
