import signal
from secret import flag
from Crypto.Random import random
from Crypto.Util.number import getPrime

#Odds and evens (hand game)
#https://en.wikipedia.org/wiki/Odds_and_evens_(hand_game)

def pad(choice, n):
	return 2*random.randint(1, n//2 - 1) + choice

def send(choice, n):
	choice = pad(choice, n)
	return pow(2, choice, n )

signal.alarm(360)
print ("Let's play odds and evens! If I win you loose 5 times the amount of money you have bet! I choose odd.\n")

WALLET = 10
while WALLET > 0:
	print("Your current wallet is {} $.\n".format(WALLET))

	if WALLET > 133337:
		print("Wow, You've got filthy rich. Here's your flag: {}".format(flag))
		exit()

	n = getPrime(1024)*getPrime(1024)
	print ("Public Modulus : {}\n".format(n))

	bet = int(input("Place your bet : "))
	assert bet <= WALLET and bet > 0

	choice = random.randint(0, 5)
	print ("Here's my choice : {}\n".format(send(choice, n)))

	player = int(input("Shilaaafooooooormi: "))
	assert player >= 0 and player < 6

	if (choice + player ) & 1:
		print("You lose.")
		WALLET -= 5*bet
	else:
		print("You win.")
		WALLET += bet

print("You got no money left in your wallet. Make sure to come back later!")