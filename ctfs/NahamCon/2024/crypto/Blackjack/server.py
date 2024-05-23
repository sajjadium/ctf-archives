# A lot of this code is taken from https://github.com/rishimule/blackjack-python
from inputimeout import inputimeout, TimeoutOccurred
import os, sys

suits = ("Hearts", "Clubs", "Diamonds", "Spades")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King", "Ace")
values = {"Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5, "Six" : 6, "Seven" :7, "Eight" : 8, "Nine" : 9, "Ten" : 10, "Jack" : 10, "Queen" : 10, "King" : 10, "Ace" : 11}

class PRNG:
	def __init__(self, seed = int(os.urandom(8).hex(),16)):
		self.seed = seed
		self.state = [self.seed]
		self.index = 52
		for i in range(51):
			self.state.append((3 * (self.state[i] ^ (self.state[i-1] >> 6)) + i+1)%512)

	def __str__(self):
		return f"{self.state}"

	def getnum(self):
		if self.index >= 52:
			for i in range(52):
				y = (self.state[i] & 0x40) + (self.state[(i+1)%52] & 0x3f)
				val = y >> 1
				val = val ^ self.state[(i+9)%52]
				if y & 1:
					val = val ^ 69
				self.state[i] = val
			self.index = 0
		seed = self.state[self.index]
		self.index += 1
		return (seed*13 + 17)%(2**7)

class Card:
	def __init__(self,rank,suit):
		self.rank = rank
		self.suit = suit
		self.value = values[rank]

	def __str__(self):
		return self.rank + " of " + self.suit

class Deck:
	def __init__(self):
		self.cardlist = []
		for suit in suits:
			for rank in ranks:
				current_card = Card(rank,suit)
				self.cardlist.append(current_card)
	
	def __str__(self):
		deck_cards = ''
		for x in range(len(self.cardlist)):
			deck_cards += str(self.cardlist[x]) + "\n"
		return f"This Deck has {str(len(self.cardlist))} Cards.\n" + deck_cards
	
	def shuffle_deck(self):
		new_deck = []
		for i in range(len(self.cardlist)):
			x = rng.getnum() % 52
			if self.cardlist[x] not in new_deck:
				new_deck.append(self.cardlist[x])
			elif self.cardlist[i] not in new_deck:
				new_deck.append(self.cardlist[i])
			else:
				for card in self.cardlist:
					if card not in self.cardlist:
						new_deck.append(card)
						break
		self.cardlist = new_deck
	
	def deal_one(self):
		return self.cardlist.pop(0)

class Player:
	def __init__(self,name,chips):
		self.name = name
		self.chips = chips
		self.bet = 0
	
	def __str__(self):
		return 'Player {} has {} chips\n'.format(self.name,self.chips)
	
	def add_chips(self,chips):
		self.chips += chips
	
	def remove_chips(self,chips):
		if chips > self.chips or chips < 1:
			print("Invalid amount of Chips.")
			print("Current balance = {}".format(self.chips))
			
		else:
			self.chips -= chips
			print("Current balance = {}".format(self.chips))

class Hand:
	def __init__(self):
		self.cards = []
		self.value = 0
		self.ace_count = 0
	
	def __str__(self):
		cards_in_hand = ''
		for x in range(len(self.cards)):
			cards_in_hand += "  " + str(self.cards[x]) + "\n"
		return cards_in_hand + "This hand has a value of {}.".format(self.value)
	
	def add_card(self,card):
		self.cards.append(card)
		self.value += card.value
		if card.rank == "Ace":
			self.ace_count += 1
		while self.value > 21 and self.ace_count > 0:
			self.value -= 10
			self.ace_count -= 1

def take_bet(player):
	while True:
		try:
			current_bet = int(inputimeout(prompt="Amount of chips to bet: ", timeout=60))
			if current_bet > player.chips or current_bet < 1:
				print("Invalid amount. Please try again\n")
			else:
				player.bet += current_bet
				player.chips -= current_bet
				break
		except ValueError:
			print("That is an invalid option! Please try again\n")
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()

def create_player():
	global player
	while True:
		try:
			player_name = inputimeout("Please enter your name: ", timeout=60)
			if player_name != '':
				break
			else:
				print("Please enter a valid name\n")
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()
	player = Player(player_name,1000)

def adjust_winnings(winner):
	if winner == "player":
		player.chips += int(player.bet*1.5)
		player.bet = 0
	elif winner == "tie" :
		player.chips += player.bet
		player.bet = 0
	else:
		player.bet = 0

def hit_or_stand(player_hand,deck_1):
	while True:
		try:
			temp = inputimeout(prompt="HIT OR STAND? : ", timeout=60)
			if temp == '':
				print("Please choose a valid option\n")
			elif temp[0].lower() == 'h':
				player_hand.add_card(deck_1.deal_one())
				break
			elif temp[0].lower() == 's':
				break
			else:
				print("Please choose a valid option\n")
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()
	if temp[0].lower() == 'h':
		return "h"
	else:
		return "s"

def player_busted():
	global winner	
	print("\nPlayer Busted.")
	print("Dealer Wins!\n")
	winner = "dealer"

def dealer_busted():
	global winner
	print("\nDealer Busted.")
	print("Player Wins!\n")
	winner = "player"

def player_dealer_tie():
	global winner	
	print("IT'S A TIE!!\n")
	winner = "tie"

def player_wins():
	global winner	
	print("Player Wins!\n")
	winner = "player"
	
def dealer_wins():
	global winner
	print("Dealer Wins!\n")
	winner = "dealer"	

def show_some_cards(player_hand, dealer_hand):
	print("\nPlayer Cards are : ")
	print(str(player_hand))
	print("\nDealer Cards are : ")
	print("  " + str(dealer_hand.cards[0]))
	print("**Card is Hidden.**")
	print(50*'*')

def show_all_cards(player_hand, dealer_hand):
	print("\nPlayer Cards are : ")
	print(str(player_hand))
	print("\nDealer Cards are : ")
	print(str(dealer_hand))
	print(50*'*')

def main(player):
	deck_1=Deck()
	deck_1.shuffle_deck()
	player_hand = Hand()
	dealer_hand = Hand()
	print(50*'*')
	print(player)
	take_bet(player)
	player_hand.add_card(deck_1.deal_one())
	player_hand.add_card(deck_1.deal_one())
	dealer_hand.add_card(deck_1.deal_one())
	dealer_hand.add_card(deck_1.deal_one())
	show_some_cards(player_hand, dealer_hand)
	while True:
		if player_hand.value == 21:
			break
		elif player_hand.value > 21:
			player_busted()
			break
		req = hit_or_stand(player_hand, deck_1)
		if req == 's':
			break
		show_some_cards(player_hand, dealer_hand)
	show_all_cards(player_hand, dealer_hand)
	dealer_playing = True
	while dealer_playing:
		if player_hand.value <= 21:
			while dealer_hand.value < 17 :
				print("\nDealer Hits......")
				dealer_hand.add_card(deck_1.deal_one())
				show_all_cards(player_hand, dealer_hand)
			dealer_playing = False
			if dealer_hand.value > 21:
				dealer_busted()
				break
			elif player_hand.value == dealer_hand.value:
				player_dealer_tie()
				break
			elif player_hand.value > dealer_hand.value:
				player_wins()
				break
			else:
				dealer_wins()
				break
		else:
			break
	adjust_winnings(winner)
	print("\n" + str(player))

def play_again():
	while True:
		print(50*'*')
		try:
			temp = inputimeout(prompt="\nWant to play again? : ", timeout=60)
			if temp[0].lower() == 'y':
				return True
			elif temp[0].lower() == 'n':
				print(50*'*')
				print("\nThank you for playing...\n")
				print(50*'*')
				return False
			else:
				print("Please choose a valid option\n")
		except TimeoutOccurred:
			print("Oof! Not fast enough!\n")
			sys.exit()

if __name__ == '__main__':
	playing = True
	create_player()
	global rng
	rng = PRNG()
	while playing:
		main(player)
		if player.chips >= 1000000:
			print(50*'*')
			print("Congratulations on winning this big! Here's a special reward for that...")
			with open('flag.txt', 'r') as f:
				print(f.read())
			print("\nThank you for playing...\n")
			print(50*'*')
			break
		elif player.chips == 0:
			print(50*'*')
			print("Sorry for losing everything. Better luck next time!")
			print(50*'*')
			break
		playing=play_again()