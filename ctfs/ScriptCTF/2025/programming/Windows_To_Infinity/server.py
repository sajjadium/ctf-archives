mport random
import subprocess

n = 1000000
window_size = n / 2

"""
You will receive {n} numbers.
Every round, you will need to calculate a specific value for every window.
You will be doing the calculations on the same {n} numbers every round.
For example, in this round, you will need to find the sum of every window.

Sample testcase for Round 1 if n = 10

Input:
1 6 2 8 7 6 2 8 3 8

Output:
24 29 25 31 26 27
"""

a = []
for i in range(n):
    a.append(str(random.randint(0, 100000)))
    print(a[i], end=' ')

print()

proc = subprocess.Popen(['./solve'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

proc.stdin.write(' '.join(a) + '\n')
proc.stdin.flush()

def round(roundnumber, roundname):
    print(f"Round {roundnumber}: {roundname}!")

    ur_output = list(map(int, input().split()))

    correct_output = list(map(int, proc.stdout.readline().split()))

    if ur_output != correct_output:
        print('uh oh')
        exit(1)

round(1, "Sums")
round(2, "Xors")
round(3, "Means") # Note: means are rounded down
round(4, "Median") # Note: medians are calculated using a[floor(n / 2)]
round(5, "Modes") # Note: if there is a tie, print the mode with the largest value
round(6, "Mex (minimum excluded)") # examples: mex(5, 4, 2, 0) = 1, mex(4, 1, 2, 0) = 3, mex(5, 4, 2, 1) = 0
round(7, "# of Distinct Numbers")
round(8, "Sum of pairwise GCD") # If bounds of the window are [l, r], find the sum of gcd(a[i], a[j]) for every i, j where l <= i < j <= r, 

print(open('flag.txt', 'r').readline())
