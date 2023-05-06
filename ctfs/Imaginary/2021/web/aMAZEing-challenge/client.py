import json
import requests
from os import system
from pprint import pprint

from maze import Maze
from cookie_decoder import cookie_decode

API = "http://127.0.0.1:9001"

# IMPORTANT: 
# This is just a template, you can change it or create your own client to talk to the server.
# It's almost impossible to get the flag with the script (in unmodified form), but you can give it a try.


def parse_session(data):
	data = data["session"]
	data = cookie_decode(data).decode()
	return json.loads(data)


def get_new_maze(s):

	res = s.get(f"{API}/")  # init maze
	session = s.cookies

	data = parse_session(session)
	maze = Maze(data=data["maze"])
	
	return maze


def send_steps(s, directions):
	res = s.get(f"{API}/step?directions={directions}").text  # send direction, only update local maze
	return res


if __name__ == "__main__":
	s = requests.Session()
	maze = get_new_maze(s)

	system("clear")
	print(maze)
	print("Hello there and welcome to my aMAZEing challenge!")
	print("The flag is marked on the maze, just navigate to it and I'll give it to you.")
	input("Enter [s] for down, [w] for up, [a] for left or [d] for right to walk in the maze. Enter any key to start.\n")
	system("clear")
	print(maze)

	while True:

		directions = input("> ")
		res = send_steps(s, directions)
		
		for d in list(directions):
			maze.step(d)
			system("clear")
			print(maze)

		if maze.get_player_pos() == maze.get_flag_pos():
			print(res)
			break


