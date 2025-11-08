from random import randint
from hashlib import sha256
from secret import FLAG

V = [randint(0, 100) for i in range(5)]
M = [[V[i] * randint(0, 100) for i in range(5)] for i in range(5)]
C = [M[i // 5 % 5][i % 5] ^ ord(FLAG[i]) for i in range(len(FLAG))]

print(f"{V = }")
print(f"{C = }")
print(sha256(FLAG.encode()).digest().hex())
# V = [14, 38, 56, 76, 51]
# C = [1357, 2854, 1102, 1723, 4416, 283, 344, 4566, 5023, 1798, 477, 3833, 1839, 5416, 4017, 1066, 161, 415, 5637, 1696, 1058, 3025, 5286, 5141, 3818, 1373, 2839, 1102, 1764, 4432, 313, 322, 4545, 5012, 1835, 477, 3825]
# e256693b7b7d07e11f2f83f452f04969ea327261d56406d2d657da1066cefa17
