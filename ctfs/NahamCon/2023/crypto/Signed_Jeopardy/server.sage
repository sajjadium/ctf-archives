from random import randint
from hashlib import sha512

with open("flag.txt",'r') as f:
	flag = f.read()

questions = []
answers = []
with open('questions.txt','r') as f:
	for x in f.readlines():
		a = x.split('\t')
		questions.append(a[0])
		answers.append(a[1][:-1])

# P521 standard curve parameters
p = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151
a = 6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057148
b = 1093849038073734274511112390766805569936207598951683748994586394495953116150735016013708737573759623248592132296706313309438452531591012912142327488478985984
Gx = 2661740802050217063228768716723360960729859168756973147706671368418802944996427808491545080627771902352094241225065558662157113545570916814161637315895999846
Gy = 3757180025770020463545507224491183603594455134769762486694567779615544477440556316691234405012945539562144444537289428522585666729196580810124344277578376784
E = EllipticCurve(GF(p), [a, b])
G = E(Gx, Gy)
n = 6864797660130609714981900799081393217269435300143305409394463459185543183397655394245057746333217197532963996371363321113864768612440380340372808892707005449
k = randint(1,n-1)
d = randint(1,n-1)
Pub = d*G

def menu():
	print("\nWhat service would you like?")
	print("\t1. Question")
	print("\t2. Flag")
	print("\t3. Quit")

def sign():
	index = randint(0,len(questions)-1)
	question = questions[index]
	answer = "What is "+answers[index].upper()+"?"
	m_hash = int(sha512(answer.encode()).hexdigest(), 16)
	P = k*G
	r = int(P[0]) % n
	s = ((m_hash + (r*d))/k)%n
	print(f"Here is the question: {question}\nAnd here is the signature: ({r}, {s})")

def get_flag():
	print("Please give the message")
	message = input("")
	for a in answers:
		if a.casefold() in message.casefold():
			print("I can't have you using the answer of one of the questions as the message!")
			quit()
	print("Please give the r value of the signature")
	r_given = int(input(""))
	print("Please give the s value of the signature")
	s_given = int(input(""))
	m_hash = int(sha512(message.encode()).hexdigest(), 16)
	P = k*G
	r = int(P[0]) % n
	s = ((m_hash + (r*d))/k)%n
	if r == r_given and s == s_given:
		print(f"As promised, here's your flag --> {flag}")
		quit()
	else:
		print("Not the right signature. HAHAHA!")

def main():
	print(f"Welcome to my ECDSA Jeopardy!\nHere is the public key:\nPublic key = {Pub}\nI'll sign the answers and give them to you.")
	while True:
		menu()
		choice = int(input(""))
		if choice == 1:
			sign()
		elif choice == 2:
			get_flag()
		elif choice == 3:
			quit()
		else:
			print("Invalid choice. Please try again.")

if __name__ == "__main__":
	main()