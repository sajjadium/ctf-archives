#part of the code that used the prng
def good_prng(seed=None):
    state = seed

    while True:
        state = (state * 1103515245 + 12345) & 0x7FFFFFFF
        yield state
arr0 = [0] * len(flag)
arr1 = [0] * len(flag)

prng = good_prng(seed_value)
for i in range(len(flag)):
    arr0[i] = next(prng) % 128
    arr1[i] = next(prng) % 128