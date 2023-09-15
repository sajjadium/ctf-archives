from inputimeout import inputimeout, TimeoutOccurred
import os, sys
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes
from math import gcd

card_value_dict = {0: "Zero", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace", 15: "Joker"}
card_rank_dict = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10, "Jack": 11, "Queen": 12, "King": 13, "Ace": 14, "Joker": 15}

class PRNG:
	def __init__(self, seed = int(os.urandom(8).hex(),16)):
		self.seed = seed
		self.state = [self.seed]
		self.index = 64
		for i in range(63):
			self.state.append((3 * (self.state[i] ^ (self.state[i-1] >> 4)) + i+1)%64)
	
	def __str__(self):
		return f"{self.state}"
	
	def getnum(self):
		if self.index >= 64:
			for i in range(64):
				y = (self.state[i] & 0x20) + (self.state[(i+1)%64] & 0x1f)
				val = y >> 1
				val = val ^ self.state[(i+42)%64]
				if y & 1:
					val = val ^ 37
				self.state[i] = val
			self.index = 0
		seed = self.state[self.index]
		self.index += 1
		return (seed*15 + 17)%(2**6)

class Card:
	def __init__(self, suit, rank):
		self.suit = suit
		self.value = card_value_dict[rank]
		self.rank = rank
	
	def __str__(self):
		return f"{self.value} of {self.suit}"

rng = PRNG()
with open('flag.txt', 'rb') as f:
	flag = f.read()

def display_hand(hand):
	hand_str = ""
	for i in range(4):
		hand_str += (str(hand[i]) + ", ")
	return hand_str+str(hand[4])

def card_str_to_Card(card_str):
	card_array = card_str.split(" ")
	return Card(card_array[2], card_rank_dict[card_array[0]])

def hand_scorer(hand):
	hand.sort(key=lambda x: x.rank, reverse=True)
	ranks = [card.rank for card in hand]
	suits = [card.suit for card in hand]
	is_flush = len(set(suits))==1
	is_straight = len(set(ranks))==5 and max(ranks)-min(ranks)==4
	is_four_kind = any([len(set(ranks[i:i+4]))==1 and len(set(suits[i:i+4]))==4 for i in range(2)])
	is_full_house = (len(set(ranks[0:3]))==1 and len(set(suits[0:3]))==3 and len(set(ranks[3:5]))==1 and len(set(suits[3:5]))==2) or (len(set(ranks[0:2]))==1 and len(set(suits[0:2]))==2 and len(set(ranks[2:5]))==1 and len(set(suits[2:5]))==3)
	is_three_kind = (not is_four_kind) and (not is_full_house) and any([len(set(ranks[i:i+3]))==1 and len(set(suits[i:i+3]))==3 for i in range(3)])
	pair_array = [len(set(ranks[i:i+2]))==1 and len(set(suits[i:i+2]))==2 for i in range(4)]
	if is_flush and is_straight:
		if ranks[0] == 15:
			return 9, hand, "Royal Flush"
		else:
			return 8, hand, "Straight Flush"
	elif is_four_kind:
		return 7, hand, "Four of a kind"
	elif is_full_house:
		return 6, hand, "Full House"
	elif is_flush:
		return 5, hand, "Flush"
	elif is_straight:
		return 4, hand, "Straight"
	elif is_three_kind:
		return 3, hand, "Three of a kind"
	elif sum(pair_array)==2:
		return 2, hand, "Two pair"
	elif sum(pair_array)==1:
		return 1, hand, "One pair"
	else:
		return 0, hand, "High card" 

def determine_winner(computer_cards, player_cards):
	computer_score, computer_cards, computer_hand = hand_scorer(computer_cards)
	player_score, player_cards, player_hand = hand_scorer(player_cards)
	print(f"My hand is {display_hand(computer_cards)}\t-->\tI have a {computer_hand}")
	print(f"Your hand is {display_hand(player_cards)}\t-->\tYou have a {player_hand}")
	if computer_score > player_score:
		return [1,0]
	elif computer_score < player_score:
		return [0,1]
	else:
		if computer_score in [9, 8, 5, 4, 0]:
			for i in range(5):
				if computer_cards[i].rank > player_cards[i].rank:
					return [1,0]
				elif computer_cards[i].rank < player_cards[i].rank:
					return [0,1]
			return [0,0]
		else:
			if computer_score == 7:
				four_card_computer_rank = computer_cards[0].rank if computer_cards[0].rank==computer_cards[1].rank else computer_cards[1].rank
				leftover_computer_rank = computer_cards[4].rank if computer_cards[0].rank==computer_cards[1].rank else computer_cards[0].rank
				four_card_player_rank = player_cards[0].rank if player_cards[0].rank==player_cards[1].rank else player_cards[1].rank
				leftover_player_rank = player_cards[4].rank if player_cards[0].rank==player_cards[1].rank else player_cards[0].rank
				if four_card_computer_rank > four_card_player_rank:
					return [1,0]
				elif four_card_computer_rank < four_card_player_rank:
					return [0,1]
				elif leftover_computer_rank > leftover_player_rank:
					return [1,0]
				elif leftover_computer_rank < leftover_player_rank:
					return [0,1]
				else:
					return [0,0]
			elif computer_score == 6:
				pair_computer_rank = computer_cards[0].rank if computer_cards[2].rank==computer_cards[3].rank else computer_cards[3].rank
				pair_player_rank = player_cards[0].rank if player_cards[2].rank==player_cards[3].rank else player_cards[3].rank
				if computer_cards[2].rank > player_cards[2].rank:
					return [1,0]
				elif computer_cards[2].rank < player_cards[2].rank:
					return [0,1]
				elif pair_computer_rank > pair_player_rank:
					return [1,0]
				elif pair_computer_rank < pair_player_rank:
					return [0,1]
				else:
					return [0,0]
			elif computer_score == 3:
				triple_computer_rank, triple_player_rank = -1, -1
				card1_computer_rank, card1_player_rank = -1, -1
				card2_computer_rank, card2_player_rank = -1, -1
				if computer_cards[0].rank == computer_cards[1].rank == computer_cards[2].rank:
					triple_computer_rank = computer_cards[0].rank
					card1_computer_rank = computer_cards[3].rank
					card2_computer_rank = computer_cards[4].rank
				elif computer_cards[1].rank == computer_cards[2].rank == computer_cards[3].rank:
					triple_computer_rank = computer_cards[1].rank
					card1_computer_rank = computer_cards[0].rank
					card2_computer_rank = computer_cards[4].rank
				else:
					triple_computer_rank = computer_cards[2].rank
					card1_computer_rank = computer_cards[0].rank
					card2_computer_rank = computer_cards[1].rank
				if player_cards[0].rank == player_cards[1].rank == player_cards[2].rank:
					triple_player_rank = player_cards[0].rank
					card1_player_rank = player_cards[3].rank
					card2_player_rank = player_cards[4].rank
				elif player_cards[3].rank == player_cards[1].rank == player_cards[2].rank:
					triple_player_rank = player_cards[1].rank
					card1_player_rank = player_cards[0].rank
					card2_player_rank = player_cards[4].rank
				else:
					triple_player_rank = player_cards[2].rank
					card1_player_rank = player_cards[0].rank
					card2_player_rank = player_cards[1].rank
				if triple_computer_rank > triple_player_rank:
					return [1,0]
				elif triple_computer_rank < triple_player_rank:
					return [0,1]
				elif card1_computer_rank > card1_player_rank:
					return [0,1]
				elif card1_computer_rank < card1_player_rank:
					return [1,0]
				elif card2_computer_rank > card2_player_rank:
					return [0,1]
				elif card2_computer_rank < card2_player_rank:
					return [1,0]
				else:
					return [0,0]
			elif computer_score == 2:
				pair1_computer_rank, pair1_player_rank = computer_cards[1].rank, player_cards[1].rank
				pair2_computer_rank, pair2_player_rank = computer_cards[3].rank, player_cards[3].rank
				leftover_computer_rank, leftover_player_rank = -1, -1
				if computer_cards[1].rank == computer_cards[2].rank:
					leftover_computer_rank = computer_cards[0].rank
				elif computer_cards[3].rank == computer_cards[2].rank:
					leftover_computer_rank = computer_cards[4].rank
				else:
					leftover_computer_rank = computer_cards[2].rank
				if player_cards[1].rank == player_cards[2].rank:
					leftover_player_rank = player_cards[0].rank
				elif player_cards[3].rank == player_cards[2].rank:
					leftover_player_rank = player_cards[4].rank
				else:
					leftover_player_rank = player_cards[2].rank
				if pair1_computer_rank > pair1_player_rank:
					return [1,0]
				elif pair1_computer_rank < pair1_player_rank:
					return [0,1]
				if pair2_computer_rank > pair2_player_rank:
					return [1,0]
				elif pair2_computer_rank < pair2_player_rank:
					return [0,1]
				elif leftover_computer_rank > leftover_player_rank:
					return [1,0]
				elif leftover_computer_rank < leftover_player_rank:
					return [0,1]
				else:
					return [0,0]
			else:
				pair_computer_rank, pair_player_rank = -1, -1
				leftover_computer_cards, leftover_player_cards = [], []
				if computer_cards[0].rank == computer_cards[1].rank:
					pair_computer_rank = computer_cards[0].rank
					leftover_computer_cards = computer_cards[2:]
				elif computer_cards[2].rank == computer_cards[1].rank:
					pair_computer_rank = computer_cards[1].rank
					leftover_computer_cards = [computer_cards[0]] + computer_cards[3:]
				elif computer_cards[2].rank == computer_cards[3].rank:
					pair_computer_rank = computer_cards[2].rank
					leftover_computer_cards = computer_cards[0:2] + [computer_cards[4]]
				else:
					pair_computer_rank = computer_cards[3].rank
					leftover_computer_cards = computer_cards[0:3]
				if player_cards[0].rank == player_cards[1].rank:
					pair_player_rank = player_cards[0].rank
					leftover_player_cards = player_cards[2:]
				elif player_cards[2].rank == player_cards[1].rank:
					pair_player_rank = player_cards[1].rank
					leftover_player_cards = [player_cards[0]] + player_cards[3:]
				elif player_cards[2].rank == player_cards[3].rank:
					pair_player_rank = player_cards[2].rank
					leftover_player_cards = player_cards[0:2] + [player_cards[4]]
				else:
					pair_player_rank = player_cards[3].rank
					leftover_player_cards = player_cards[0:3]
				if pair_computer_rank > pair_player_rank:
					return [1,0]
				elif pair_computer_rank < pair_player_rank:
					return [0,1]
				else:
					for i in range(3):
						if leftover_computer_cards[i].rank > leftover_player_cards[i].rank:
							return [1,0]
						elif leftover_computer_cards[i].rank < leftover_player_cards[i].rank:
							return [0,1]
					return [0,0]

def shuffle(deck):
	new_deck = []
	for i in range(len(deck)):
		x = rng.getnum()
		if deck[x] not in new_deck:
			new_deck.append(deck[x])
		elif deck[i] not in new_deck:
			new_deck.append(deck[i])
		else:
			for card in deck:
				if card not in new_deck:
					new_deck.append(card)
					break
	return new_deck

def main():
	deck = []
	deck_str = []
	for suit in ["Spades", "Hearts", "Diamonds", "Clubs"]:
		for i in range(16):
			deck.append(Card(suit, i))
			deck_str.append(str(deck[-1]))
	streak = 0
	p = getPrime(300)
	q = getPrime(300)
	phi = (p-1)*(q-1)
	N = p*q
	print(f"Let's play some mental poker!\nIf you win 10 consecutive times, I'll give you a prize!\nHere are the primes we will use to generate our RSA public and private exponents --> {p}, {q}")
	while True:
		print("What is your public exponent?")
		try:
			player_e = int(inputimeout(prompt='>> ', timeout=60))
			if gcd(player_e, phi) == 1:
				break
			else:
				print("That is an invalid public exponent! Please try again\n")
		except ValueError:
			print("That is an invalid option! Please try again\n")
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()
	print("Since you have access to my source code and know that I am trust-worthy, please give me the private exponent as well so that I will do all the calculations for us")
	while True:
		print("What is your private exponent?")
		try:
			player_d = int(inputimeout(prompt='>> ', timeout=60))
			if (player_e*player_d)%phi == 1:
				break
			else:
				print("That is an invalid private exponent! Please try again\n")
		except ValueError:
			print("That is an invalid option! Please try again\n")
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()
	round_counter = 1
	computer_e, computer_d = -1, 0
	while streak < 10:
		print(f"\n{'*'*10} Round {round_counter}, current streak is {streak} {'*'*10}")
		deck = shuffle(deck)
		assert len(set(deck)) == len(deck_str)
		while computer_e < 2 or computer_d < 1:
			e_array = []
			for _ in range(6):
				e_array.append(str(rng.getnum()))
			computer_e = int(''.join(e_array))
			if gcd(computer_e, phi) == 1:
				computer_d = pow(computer_e,-1,phi)
		enc_deck = []
		for card in deck:
			enc_deck.append(pow(pow(bytes_to_long(str(card).encode()),computer_e,N),player_e,N))
		assert len(set(enc_deck)) == len(deck_str)
		print(f"Here is the shuffled encrypted deck --> {enc_deck}")
		print("Please shuffle the deck and give it back to me one card at a time")
		shuffled_deck = []
		for x in range(len(enc_deck)):
			while True:
				try:
					enc_card = int(inputimeout(prompt=f'Card {x+1} >> ', timeout=60))
					if enc_card in enc_deck:
						card = long_to_bytes(pow(pow(enc_card,computer_d,N),player_d,N)).decode()
						assert card in deck_str
						shuffled_deck.append(card_str_to_Card(card))
						break
					else:
						print("That is an invalid card! Please try again\n")
				except ValueError:
					print("That is an invalid option! Please try again\n")
				except TimeoutOccurred:
					print("Oof! Not fast enough!\n")
					sys.exit()
		assert len(set(shuffled_deck)) == len(deck_str)
		deck = shuffled_deck
		computer_cards, player_cards = deck[0:5], deck[5:10]
		computer_winner, player_winner = determine_winner(computer_cards, player_cards)
		if not computer_winner and not player_winner:
			print("It is a tie!")
		elif computer_winner:
			print("I win!")
			streak = 0
		elif player_winner:
			print("You win!")
			streak += 1
		round_counter += 1
	if streak == 10:
		print("Congraulations! You got a 10 game streak!")
		print(f"But I don't trust that you did not cheat and so, here's the encrypted flag. HAHAHAHA!!!!")
		print(long_to_bytes(pow(bytes_to_long(flag),computer_e,N)))
		print()

if __name__ == "__main__":
	main()
