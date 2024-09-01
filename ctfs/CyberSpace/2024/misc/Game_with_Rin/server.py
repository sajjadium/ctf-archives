from basement_of_rin import NanakuraRin, flag, generate_graph

import time
from random import Random

def Server(m):
	print("Server> " + m)

def Rin(m):
	print("Rin> " + m)

def check_subset(_subset, set):
	subset = sorted(_subset)
	assert len(subset) != 0
	for i in range(len(subset) - 1):
		subset[i] < subset[i + 1]
	for x in subset:
		assert x in set

class disjoint_set:
	def __init__(self, n):
		self.n = n
		self.p = [-1] * self.n
	def root(self, u):
		if self.p[u] < 0:
			return u
		self.p[u] = self.root(self.p[u])
		return self.p[u]
	def share(self, u, v):
		return self.root(u) == self.root(v)
	def merge(self, u, v):
		u, v = self.root(u), self.root(v)
		if u == v:
			return False
		if self.p[u] > self.p[v]:
			u, v = v, u
		self.p[u] += self.p[v]
		self.p[v] = u
		return True
	def clear(self):
		self.p = [-1] * self.n

def check_tree(subset, V, edges):
	assert len(subset) == V - 1
	ds = disjoint_set(V)
	for i in subset:
		assert isinstance(i, int) and 0 <= i < len(edges)
		u, v, w = edges[i]
		assert ds.merge(u, v)

def determine_the_winner(piles):
	# https://en.wikipedia.org/wiki/Nim
	# Rin-chan is perfect, so she'll always make the optimal move.
	# You're perfect too, so you'll always make the perfect move as well.
	# Let's fast-forward the game to the end :)
	nim = 0
	for x in piles:
		nim ^= x
	return "first" if nim != 0 else "second"

class You:
	def __init__(self, V, edges):
		Server(f"{V = }")
		Server(f"{edges = }")
	def first_move(self):
		Server("Please choose S")
		return sorted(list(map(int, input("You> S = ").strip().split(" "))))
	def read_first_move(self, S):
		Rin(f"I choose S = {' '.join([str(i) for i in S])}")
	def second_move(self):
		Server("Please choose T")
		return sorted(list(map(int, input("You> T = ").strip().split(" "))))

Rin("Do you want this flag?")
Rin("I'll consider giving it to you if you defeat me 200 times :)")

time.sleep(0.5)

Server("-----------------------------------------------------------------------------------------")
Server("[Round Manual]")
Server("1. The server generates a set of edges with integer weight on vertices 0 ~ V-1.")
Server("2. You can either choose to go first or second.")
Server("3. First player chooses a subset S of edges of size V-1 which forms a tree.")
Server("( For the definition of tree, see https://en.wikipedia.org/wiki/Tree_(graph_theory) )")
Server("4. Second player chooses a non-empty subset T of S.")
Server("5. Add a pile consisting of w stones for each edge (u, v, w) in T.")
Server("6. Winner of the round is the winner of the nim game on those set of piles.")
Server("-----------------------------------------------------------------------------------------")

time.sleep(0.5)

Rin("GLHF!")

time.sleep(0.5)

for round_number in range(1, 201):
	Server(f"Round {round_number}")

	V, edges = generate_graph(round_number)
	assert isinstance(V, int)
	assert 30 <= V <= 200
	assert len(edges) <= 300
	for u, v, w in edges:
		assert isinstance(u, int) and isinstance(v, int) and isinstance(w, int)
		assert 0 <= u < V and 0 <= v < V and 0 <= w < 2**(V-1)

	first, second = You(V, edges), NanakuraRin(V, edges)
	
	Rin("Do you want to go [first] or [second]?")
	resp = input("You> ").strip()
	if resp not in ["first", "second"]:
		Rin("That's not an option >:(")
		exit(0)

	if resp == "first":
		Rin("Sure, you go first :D")
	else:
		Rin("Ok, I go first :D")
		first, second = second, first

	S = first.first_move()
	second.read_first_move(S)
	check_subset(S, [i for i in range(len(edges))])
	check_tree(S, V, edges)

	if resp == "first":
		Rin("My turn!")
	else:
		Rin("Your turn!")

	T = second.second_move()
	check_subset(T, S)

	if resp == "first":
		Rin(f"I choose T = {' '.join([str(i) for i in T])}")

	winner = determine_the_winner([edges[i][2] for i in T])

	r = Random()

	if winner != resp:
		Rin(r.choice(["Git gud", "Noob", "Easy"]))
		exit(0)

	Rin(r.choice(["Not like this!", "You won :(", "Ouch!", "You got lucky this time."]))

Rin("GG Well played!")
Rin("I guess I have no choice but to give you the flag.")
Rin(f"{flag}")