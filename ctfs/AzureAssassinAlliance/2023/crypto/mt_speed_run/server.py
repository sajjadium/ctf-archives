import random, os, hashlib, base64, signal
from secret import FLAG

sys_rng = random.SystemRandom()
def rand_magic():
    while True:
        value = sys_rng.getrandbits(32)
        if 10 <= bin(value).count('1') <= 22:
            return value

MAGIC_A = rand_magic()
MAGIC_B = rand_magic()
MAGIC_C = rand_magic()
MAGIC_D = rand_magic()
MAGIC_E = sys_rng.randrange(0, 32)

# YES, YOU HAVE SEEN THIS PROBLEM MANY TIMES

N = 624
NN = 30000

def temper(state):
    y = state
    y ^= y >> 11
    y ^= (y << 7) & MAGIC_A
    y ^= (y << 15) & MAGIC_B
    y ^= (y << MAGIC_E) & MAGIC_D
    y ^= y >> 18
    return y

def update_mt(mt):
    M = 397
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7FFFFFFF
    for kk in range(N - M):
        y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
        mt[kk] = mt[kk + M] ^ (y >> 1) ^ (y % 2) * MAGIC_C
    for kk in range(N - M, N - 1):
        y = (mt[kk] & UPPER_MASK) | (mt[kk + 1] & LOWER_MASK)
        mt[kk] = mt[kk + (M - N)] ^ (y >> 1) ^ (y % 2) * MAGIC_C
    y = (mt[N - 1] & UPPER_MASK) | (mt[0] & LOWER_MASK)
    mt[N - 1] = mt[M - 1] ^ (y >> 1) ^ (y % 2) * MAGIC_C

state = [sys_rng.getrandbits(32) for _ in range(N)]
state_i = 0
def next_rand():
    global state, state_i
    ret = temper(state[state_i]) >> 31
    state_i += 1
    if state_i >= 624:
        state_i -= 624
        update_mt(state)
    return ret

update_mt(state)
rands = [next_rand() for _ in range(NN)]
ans = hashlib.sha256(','.join(map(str, state)).encode()).hexdigest()
print('RANDS = {}'.format(base64.b64encode(int(''.join(map(str, rands)), 2).to_bytes(NN // 8, 'big')).decode()))

time_out = False
def handler(_signum, _frame):
    global FLAG, time_out
    FLAG = None
    time_out = True

signal.signal(signal.SIGALRM, handler)
signal.alarm(10)

print(f'{MAGIC_A = :#x}')
print(f'{MAGIC_B = :#x}')
print(f'{MAGIC_C = :#x}')
print(f'{MAGIC_D = :#x}')
print(f'{MAGIC_E = :#x}')

if input('ANS = ') == ans:
    if time_out:
        print('CONTINUE OPTIMIZE!!!')
    else:
        print('FLAG = {}'.format(FLAG))
else:
    print('CONTINUE DEBUGGING!!!')