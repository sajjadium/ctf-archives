from functools import reduce
import sys


def KekF1601onLanes(lanes):
    R = 1
    for _ in range(24):
        C = [reduce(lambda a, b: a ^ b, lanes[x]) for x in range(len(lanes))]
        D = [
            C[(x + 4) % len(lanes)] ^ C[(x + 1) % len(lanes)] for x in range(len(lanes))
        ]

        lanes = [[lanes[x][y] ^ D[y] for y in range(8)] for x in range(len(lanes))]

        for i in range(len(lanes)):
            aux = lanes[i][0]
            for j in range(len(lanes[0]) - 1):
                lanes[i][j] = lanes[i][j + 1]
            lanes[i][-1] = aux

        aux = lanes[0]
        for j in range(len(aux)):
            for i in range(len(lanes) - 1):
                lanes[i][j] = lanes[i][j] ^ lanes[i + 1][j]
            lanes[-1][j] = lanes[-1][j] ^ aux[j]

        R = ((R << 1) ^ ((R >> 7) * 0x71)) % 256
        lanes[0][0] ^= R & 2
    return lanes


def KekF1601(state):
    lanes = [state[x * 8 : (x + 1) * 8] for x in range(len(state) // 8)]
    lanes = KekF1601onLanes(lanes)
    state = [item for row in lanes for item in row]

    return state


OUT_LEN = 69


def Kek(rate, state, delimitedSuffix):
    rateInBytes = rate // 8
    blockSize = 69

    state[blockSize] = state[blockSize] ^ delimitedSuffix
    state[rateInBytes - 1] = state[rateInBytes - 1] ^ 0x80
    state = KekF1601(state)

    return state[0:OUT_LEN]


def SAH3_652(state_arr):
    return Kek(1088, state_arr, 0x06)


state0 = list(sys.argv[1].encode("utf-8"))  # Flag
state0.extend([0] * (200 - len(state0)))
out = SAH3_652(state0)
print(bytes(out).hex())

# 2033251f4b3161e4455a4c261e3f631e18653c3a6c136e30304037373e6e1f6c6f6448673e686b1e18603d10306d323f3a4b626eee636c3c3c62483592123e6d6c6c3a49ca
