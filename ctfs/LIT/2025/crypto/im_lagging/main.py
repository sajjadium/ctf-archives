import random

def lcg_generate(seed, a, c, m, total):
    xs = [seed]
    for _ in range(total - 1):
        xs.append((a * xs[-1] + c) % m)
    return xs

def lfg_from_lcg(xs, lags, m, total):
    lfg = xs
    for i in range(total):
        s = sum(lfg[-1*lag] for lag in lags) % m
        lfg.append(s)
    return lfg

def generate_challenge(n_lags=50, m=2**59-1, total_needed=10000):
    max_lag = 10000
    lags = sorted(random.sample(range(1, max_lag + 1), n_lags))
    seed = random.randint(0, m-1)
    a = random.randint(2, m - 1)
    c = random.randint(0, m - 1)

    xs = lcg_generate(seed, a, c, m, total_needed)
    ys = lfg_from_lcg(xs, lags, m, total_needed+1)

    return {
    'lfg_outputs': ys[-1*(total_needed+1):-1],
    'next_lfg_output': ys[-1]
    }

challenge = generate_challenge()

input("Press enter to receive LFG output: ")
print(' '.join(map(str, challenge['lfg_outputs'])))

guess = input("\nYour guess for the next LFG output: ")
guess = int(guess)
if guess == challenge['next_lfg_output']:
    print("Correct")
    with open("flag.txt", "r") as f:
        print(f.read())
else:
    print("Wrong")