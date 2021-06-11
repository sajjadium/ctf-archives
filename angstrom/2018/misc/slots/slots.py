# coding: utf8	

import random
import signal
import SocketServer

flag = open('flag.txt').read()

PORT = 3002

FRUITS = ['🍌', '🍒', '🍐', '🍈', '🍇', '🍊', '🍉']
COMBOS = {
	'🍌3': 1,
	'🍒2': 1,
	'🍐2': 3,
	'🍈2': 3,
	'🍇2': 3,
	'🍊2': 3,
	'🍉2': 3,
	'🍒3': 3,
	'🍐3': 10,
	'🍈3': 10,
	'🍇3': 10,
	'🍊3': 10,
	'🍉3': 10
}

def line():
	return [random.choice(FRUITS) for i in range(3)]

def payout(line):
	for fruit in line:
		combo = fruit + str(line.count(fruit))
		if combo in COMBOS:
			return COMBOS[combo]
	return 0

class incoming(SocketServer.BaseRequestHandler):
	def handle(self):
		req = self.request

		def receive():
			buf = ''
			while not buf.endswith('\n'):
				buf += req.recv(1)
			return buf[:-1]

		signal.alarm(60)
		
		req.sendall('Welcome to Fruit Slots!\n')
		req.sendall('We\'ve given you $10.00 on the house.\n')
		req.sendall('Once you\'re a high roller, we\'ll give you a flag.\n')

		money = 10
		while True:
			req.sendall('You have ${0:.2f}.\n'.format(money))
			req.sendall('Enter your bet: ')
			bet = receive()

			try:
				bet = float(bet)
			except:
				req.sendall('Your bet must be a number!\n')
				req.close()
				return

			if bet <= 0:
				req.sendall('Sneaky, but not good enough.\n')
				req.close()
				return
			elif bet > money:
				req.sendall('You don\'t have enough money to wager this.\n')
				req.close()
				return

			line1 = line()
			line2 = line()
			line3 = line()
			while payout(line2):
				line2 = line()
			win = bet * payout(line2)
			money += win - bet

			req.sendall('{}\n{} ◀\n{}\n'.format(' : '.join(line1), ' : '.join(line2), ' : '.join(line3)))

			if win > 0:
				req.sendall('You won ${0:.2f}!'.format(win))
			else:
				req.sendall('You lost everything.\n')

			if money <= 0:
				req.sendall('You have no money left. Low roller.\n')
				req.close()
				return
			elif money < 1000000000:
				req.sendall('Play more to become a high roller!\n')
			else:
				req.sendall('Wow, you\'re a high roller!\n')
				req.sendall('A flag: {}\n'.format(flag))
				return

class ReusableTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
	pass

SocketServer.TCPServer.allow_reuse_address = True
server = ReusableTCPServer(('0.0.0.0', PORT), incoming)

print 'Server listening on port %d' % PORT
server.serve_forever()
