import random
from secret import flag

assert flag[: 5] == b"idek{"
assert flag[-1:] == b"}"

L = len(flag[5: -1])
print(f"L = {L}")
coeff = list(flag[5: -1])
points = random.sample(range(L), L // 2)
evaluations = []

for p in points:
	evaluations += [sum(c * p ** i for i, c in enumerate(coeff))]

print(f"points = {points}")
print(f"evaluations = {evaluations}")
