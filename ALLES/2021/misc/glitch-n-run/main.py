#!/usr/bin/python3
from re import template
from sys import argv
from Game import Game

if len(argv) <= 1 or argv[1] not in ["game", "replay", "check"]:
  print("./main.py <mode>")
  print("possible modes: game, replay, check")
  exit(0)

mode = argv[1]

game = Game(mode)

while True:
  if not game.tick():
    break

if game.won():
  print("WON!")
  if mode == "check":
    print(open("./flag.txt", "r").read())
elif game.died():
  print("Died :C")
elif game.reachedEndOfReplay():
  print("Reached end of replay input")
else:
  print("Closed window")

if game.mode == "check":
  print(f"FLAGS COLLECTED: {len(game.playerGroup.sprites()[0].flagsCollected)}")
  print(f"TICKS: {game.input.pos}")

del game
