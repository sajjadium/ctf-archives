import random
import sys
import subprocess
import time

n = 100

grid_lines = []
for _ in range(n):
    row = []
    for _ in range(n):
        flip = random.randint(1, 2)
        if flip == 1:
            row.append(str(random.randint(1, 696) * 2))
        else:
            row.append(str(random.randint(1, 696) * 5))
    grid_lines.append(' '.join(row))

for line in grid_lines:
    sys.stdout.write(line + '\n')

start = int(time.time())


proc = subprocess.run(['./solve'], input='\n'.join(grid_lines).encode(), stdout=subprocess.PIPE)
ans = []
all_ans = proc.stdout.decode()
for line in all_ans.split('\n')[:100]:
    ans.append(list(map(int, line.strip().split(' '))))

ur_output = []
for i in range(n):
    ur_output.append(list(map(int, input().split())))

if int(time.time()) - start > 20:
    print("Time Limit Exceeded!")
    exit(-1)

if ur_output == ans:
    with open('flag.txt', 'r') as f:
        print(f.readline())
else:
    print("Wrong Answer!")
