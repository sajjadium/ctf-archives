import random

random.seed(69)  # Nothing up my sleeve...

__all__ = [
    "INIT_PERM",
    "FINAL_PERM",
    "KEY_PERM1",
    "KEY_PERM2",
    "SHIFTS",
    "EXP_PERM",
    "SBOX",
    "FEISTEL_PERM",
]

INIT_PERM = tuple(random.sample(range(54), 54))
FINAL_PERM = tuple(INIT_PERM.index(i) for i in range(54))

# May have overcomplicated things...
KEY_PERM1 = [0] * 48
for i in range(54):
    if i % 9 == 8:
        continue
    a, b = divmod(i, 9)
    KEY_PERM1[b * 6 + 5 - a] = i
KEY_PERM1[24:] = KEY_PERM1[42:] + KEY_PERM1[36:42] + KEY_PERM1[30:36] + KEY_PERM1[24:30]
KEY_PERM1 = tuple(KEY_PERM1)
KEY_PERM2 = tuple(random.sample(range(24), 18) + random.sample(range(24, 48), 18))
SHIFTS = (1, 2, 2, 1, 2, 2, 1, 2)

temp = tuple(range(27))
EXP_PERM = sum((temp[i : i + 3] + (temp[(i + 3) % 27],) for i in range(0, 27, 3)), ())
SBOX = tuple(
    sum((tuple(random.sample(range(27), 27)) for _ in range(3)), ()) for _ in range(9)
)  # Nothing here this time :)
FEISTEL_PERM = tuple(random.sample(range(27), 27))
