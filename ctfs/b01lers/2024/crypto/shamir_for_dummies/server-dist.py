import os
import sys
import time
import math
import random
from Crypto.Util.number import getPrime, isPrime, bytes_to_long, long_to_bytes

def polynomial_evaluation(coefficients, x):
	at_x = 0
	for i in range(len(coefficients)):
		at_x += coefficients[i] * (x ** i)
		at_x = at_x % p
	return at_x

flag = b'bctf{REDACTED}'

print("")
print("Thanks for coming in. I can really use your help.\n")
print("Like I said, my friend can only do additions. He technically can do division but he says he can only do it once a day.")
print("")
print("I need to share my secret using Shamir secret sharing. Can you craft the shares, in a way that my friend can recover it?\n")
print("")
print("Don't worry, I have the polynomial and I will do all the math for you.")
print("")

s = bytes_to_long(flag)

n = getPrime(4)
p = getPrime(512)

while p % n != 1:
    p = getPrime(512)

print("Let's use \n")
print("n =", n)
print("k =", n)
print("p =", p)
print("")

coefficients = [s]
for i in range(1, n):
	coefficients.append(random.randint(2, p-1))

print("Okay, I have my polynomial P(X) ready. Let me know when you are ready to generate shares with me.\n")
print("")

evaluation_points = []
shares = []

count = 1
while count < n+1:
	print("Evaluate P(X) at X_{0} =".format(count))
	print("> ", end="")
	eval_point = int(input())
	if eval_point % p == 0:
		print("Lol, nice try. Bye.")
		exit()
		break
	elif eval_point < 0 or eval_point > p:
		print("Let's keep things in mod p. Please choose it again.")
	else:
		if eval_point not in evaluation_points:
			evaluation_points.append(eval_point)
			share = polynomial_evaluation(coefficients, eval_point)
			shares.append(share)
			count += 1
		else:
			print("You used that already. Let's use something else!")

print("Nice! Let's make sure we have enough shares.\n")
assert len(shares) == n
assert len(evaluation_points) == n
print("It looks like we do.\n")
print("By the way, would he have to divide with anything? (Put 1 if he does not have to)")
print("> ", end="")
some_factor = int(input())
print("Good. Let's send those over to him.")

for _ in range(3):
	time.sleep(1)
	print(".")
	sys.stdout.flush()

sum_of_shares = 0

for s_i in shares:
	sum_of_shares += s_i
	sum_of_shares = sum_of_shares % p

sum_of_shares_processed = (sum_of_shares * pow(some_factor, -1, p)) % p

if sum_of_shares_processed == s:
	print("Yep, he got my secret message!\n")
	print("The shares P(X_i)'s were':")
	print(shares)
	print("... Oh no. I think now you'd know the secret also... Thanks again though.")
else:
	print("Sorry, it looks like that didn't work :(")
