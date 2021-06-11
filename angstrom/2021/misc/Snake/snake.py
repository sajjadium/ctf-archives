#!/usr/bin/python3 -SIEs

import curses
import random
import base64
import pickle
import io

class SnakeSave:
	def __init__(self, highScores, game=None):
		self.highScores = highScores
		self.game = game

	class HighScores:
		def __init__(self, player):
			self.player = player
			self.scores = []

		def getHighScore(self, score):
			return max(self.scores+[score])

	class Game:
		def __init__(self, width, height, coords):
			self.width = width
			self.height = height
			self.coords = coords
			self.direction = curses.KEY_RIGHT
			self.score = 0
			self.food = (random.randint(1, self.height-2), random.randint(1, self.width-2))
			while self.food in self.coords: self.food = (random.randint(1, self.height-2), random.randint(1, self.width-2))

		def move(self):
			self.coords.append((
				self.coords[-1][0] + (1 if self.direction == curses.KEY_DOWN else -1 if self.direction == curses.KEY_UP else 0),
				self.coords[-1][1] + (1 if self.direction == curses.KEY_RIGHT else -1 if self.direction == curses.KEY_LEFT else 0)
			))
			if self.coords[-1][0] > 18 or self.coords[-1][1] > 58 or \
			   self.coords[-1][0] < 1 or self.coords[-1][1] < 1 or \
			   self.coords.index(self.coords[-1]) != len(self.coords) - 1: return False
			if self.food == self.coords[-1]:
				self.score += 1
				while self.food in self.coords: self.food = (random.randint(1, self.height-2), random.randint(1, self.width-2))
				return None
			else:
				erase = self.coords[0]
				self.coords = self.coords[1:]
				return erase

class SnakeRestrictedUnpickler(pickle.Unpickler):
	def find_class(self, module, name):
		if module == "__main__" and name.startswith("Snake") and name.count(".") <= 1 and len(name) <= len("SnakeSave.HighScores"):
			return super().find_class(module, name)
		raise pickle.UnpicklingError(f"HACKING DETECTED")

def SnakeWindow(_):
	curses.curs_set(0)
	win = curses.newwin(20, 60, 0, 0)
	win.border(0)
	win.keypad(1)
	win.timeout(100)
	win.addch(game.food[0], game.food[1], '*')
	for coord in game.coords: win.addch(coord[0], coord[1], '#')
	while True:
		win.addstr(0, 2, f"{highScores.player}'s Score: {game.score:05d}")
		win.addstr(0, 41, f"High Score: {highScores.getHighScore(game.score):05d}")
		key = win.getch()
		if key == 27: return True
		if key in (curses.KEY_LEFT, curses.KEY_RIGHT, curses.KEY_DOWN, curses.KEY_UP): game.direction = key
		erase = game.move()
		if erase == False: return
		elif erase: win.addch(erase[0], erase[1], ' ')
		else: win.addch(game.food[0], game.food[1], '*')
		win.addch(game.coords[-1][0], game.coords[-1][1], '#')

print('Welcome to snake! Eat as many pickles as you can. Hit a wall or yourself and you die. Press escape to resume later.')
if input('Do you have a restore code? [y/n] ')[0].lower() == 'y':
	snake = SnakeRestrictedUnpickler(io.BytesIO(base64.b64decode(input('Restore code: ')))).load()
	print(snake)
	highScores = snake.highScores
	if snake.game: game = snake.game
	else: game = SnakeSave.Game(60, 20, [(12, 12), (12, 13), (12, 14)])
else:
	highScores = SnakeSave.HighScores(input('Enter your name: '))
	game = SnakeSave.Game(60, 20, [(12, 12), (12, 13), (12, 14)])
left = curses.wrapper(SnakeWindow)
if left:
	print(f"Enter the following code to resume your game later: {base64.b64encode(pickle.dumps(SnakeSave(highScores, game))).decode('ascii')}")
else:
	highScores.scores.append(game.score)
	print(f"You ate {game.score} pickles!")
	print(f"{highScores.player}'s Top 10 Scores:")
	for num, score in enumerate(sorted(highScores.scores, reverse=True)):
		print(f"{num+1}. {score}")
		if num > 9: break
	print(f"Restore your data with the following code: {base64.b64encode(pickle.dumps(SnakeSave(highScores))).decode('ascii')}")
