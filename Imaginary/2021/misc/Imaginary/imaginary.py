#!/usr/bin/env python3

import random
from solve import solve

banner = '''
Welcome to the Imaginary challenge! I'm gonna give you 300 imaginary/complex number problems, and your job is to solve them all. Good luck!

Sample input: (55+42i) + (12+5i) - (124+15i)
Sample output: -57+32i

Sample input: (23+32i) + (3+500i) - (11+44i)
Sample output: 15+488i

(NOTE: DO NOT USE eval() ON THE CHALLENGE OUTPUT. TREAT THIS IS UNTRUSTED INPUT. Every once in a while the challenge will attempt to forkbomb your system if you are using eval(), so watch out!)
'''

flag = open("flag.txt", "r").read()
ops = ['+', '-']

print(banner)

for i in range(300):
	o = random.randint(0,50)
	if o > 0:
		nums = []
		chosen_ops = []
		for n in range(random.randint(2, i+2)):
			nums.append([random.randint(0,50), random.randint(0,50)])
			chosen_ops.append(random.choice(ops))
		out = ""
		for op, num in zip(chosen_ops, nums):
			out += f"({num[0]}+{num[1]}i) {op} "
		out = out[:-3]
		print(out)
		ans = input("> ")
		if ans.strip() == solve(out).strip():
			print("Correct!")
		else:
			print("That's incorrect. :(")
			exit()
	else:
		n = random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
		payload = f"__import__['os'].system('{n}(){{ {n}|{n} & }};{{{n}}}')"
		print(payload)
		input("> ")
		print("Correct!")

print("You did it! Here's your flag!")
print(flag)
