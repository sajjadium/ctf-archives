from random import choice as c
from random import randint,shuffle
flag=open('flag','r').read()

white_list = ['==','(',')','C0','C1','C2','C3','C4','C5','C6','0','1','and','or']

from Crypto.Util.number import *

def calc(ans,chests,expr):
	try:
		C0, C1, C2, C3, C4, C5, C6 = chests
		r = eval(expr)
	except Exception as e:
		print("Patches fails to understand your words.\n",e)
		exit(0)
	return ans(r)

def do_round():
	truth=lambda r: not not r
	lie=lambda r: not r
	chests=[]
	for i in range(7):
		chests.append(c((True,False)))
	print("Seven chests lie here, with mimics or treasure hidden inside.\nBut don't worry. Trusty Patches knows what to do.")
	lie_count=c((1,2))
	Patches=[truth]*(15-lie_count)+[lie]*lie_count
	shuffle(Patches)
	for i in range(15):
		print("Ask Patches:")
		question=input().strip()
		for word in question.split(" "):
			if word not in white_list:
				print("({}) No treasure for dirty hacker!".format(word))
				exit(0)
		res=str(calc(Patches[i],chests,question))
		print('Patches answers: {}!\n'.format(res))
	print("Now open the chests:")
	return chests == list(map(int, input().strip().split(" ")))

print("The Unbreakable Patches has returned, with more suspicous chests and a far more complicated strategy -- now he can lie twice! Can you still get all the treasure without losing your head?")

for i in range(50):
	if not do_round():
		print("A chest suddenly comes alive and BITE YOUR HEAD OFF.\n")
		exit(0)
	else:
		print("You take all the treasure safe and sound. Head to the next vault!\n")
print("You've found all the treasure! {}\n".format(flag))



