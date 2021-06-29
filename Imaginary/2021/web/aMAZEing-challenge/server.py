import random
from time import time
from base64 import b64encode
from flask import Flask, session, request, make_response

from maze import Maze
from solver import solve
from random import choice


def gen_sec_key():
	return "]!74hc_51ht_3vl0s_yltn4tsn1_ot_no155e5_wen_a_3ta3rc_tn4c_u0y_3rus_m4_I[ftci"[::-1]


def is_prime(x):
	return all(x % i for i in range(2, x))


def get_primes_between(l, u):
	return [a for a in range(l, u) if is_prime(a)]


def random_prime(l, u):
	return random.choice(get_primes_between(l, u))


def delete_session():
	for key in list(session.keys()):
		session.pop(key)


def parse_directions(directions):
	# do some super important checks, so the player can't do the "jump through walls" glitch
	if len(directions) == 3:
		
		if 3 * ord(directions[0]) - 2 * ord(directions[1]) + 1 * ord(directions[2]) == 282:
			if 4 * ord(directions[0]) - 3 * ord(directions[1]) + 2 * ord(directions[2]) == 423:
				if 1 * ord(directions[0]) - 4 * ord(directions[1]) + 3 * ord(directions[2]) == 88: 
					
					# GLITCH DETECTED, ABORT IMMEDIATELY
					delete_session()
					raise Exception("How dare you trying to cheat? Your session was deleted, you brought this to yourself!")

	return list(directions)


app = Flask(__name__)
app.config['SECRET_KEY'] = gen_sec_key()
# https://blog.miguelgrinberg.com/post/how-secure-is-the-flask-user-session
# -> everyone can read the content of the session cookie, but not change it (if the secret is secure)


FLAG = open("flag.txt", "r").read()
"""
p1 = random_prime(50, 100)
p2 = random_prime(50, 100)
flag_enc = [0x1337]
for i in range(len(FLAG)):
	flag_enc.append((flag_enc[-1] + ord(FLAG[i])) * p1 * p2)
"""
flag_enc = open("flag.txt.enc", "r").read()


@app.route('/')
def init():
	delete_session()
	maze = Maze()

	session["maze"] = str(maze)
	session["tries"] = 0

	return make_response(f"Successfully initialized a new maze. It is stored in your session cookie.")


@app.route('/step')
def step():

	# check if session still alive
	for k in ["maze", "tries"]:
		if k not in session.keys():
			return make_response("Session died! Please send a GET request to '/' to get a new and valid session!")

	# directions check
	if not request.args.get('directions'):
		return make_response("No direction(s) specified!")
	else:
		directions = parse_directions(request.args.get('directions'))

	maze = Maze(data=session["maze"])
	for d in directions:
		if d not in maze.get_actions():
			continue

		# is valid, do step
		maze.step(d)

	# all done, update maze in session
	session["maze"] = str(maze)
	session["tries"] += 1
	
	if maze.get_player_pos() == maze.get_flag_pos():
		tries = session["tries"]
		delete_session()

		if tries > 1:
			return make_response("You interacted multiple times with the '/step' endpoint. So you just get a super secure encrypted flag. Next time, try implementing Dijkstra's algorithm to solve the maze in one go, or try decrypting the flag:\n" + flag_enc)

		return make_response(FLAG)

	return make_response(f"New pos: {maze.get_player_pos()}")


@app.errorhandler(404)
def not_found(e):
	return "Invalid url! Only '/step' and '/' are allowed."


@app.errorhandler(500)
def error(e):
	return "Unexpected error occured! \nAnyways, here is your encripted flag for crashing it: " + flag_enc


if __name__ == "__main__":
	app.run(host='127.0.0.1', port=9001)