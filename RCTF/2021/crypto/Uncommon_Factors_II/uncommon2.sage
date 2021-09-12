from multiprocessing import Pool

size = 2^7

flag = open("flag.txt", "rb").read()
assert len(flag) == 22
assert flag[:5] == b"flag{"
assert flag[-1:] == b"}"
seed = flag[5:-1] # 128 bit
seed = (int.from_bytes(seed,'big')<<104) + (randint(0,2^80)<<(128+104)) # 312 bit
ub = seed + 2^104
lb = seed

threads = 64

def f(i):
    p = random_prime(ub, lbound=lb, proof=False)
    q = random_prime(2**200, proof=False)
    N = p*q
    return N

def reseed(i):
    set_random_seed()

pool = Pool(processes=threads)
pool.map(reseed,range(size))
lN = pool.map(f,range(size))
pool.close()
pool.join()

lN.sort()
with open("lN.bin","wb") as f:
    for n in lN:
        f.write(int(n).to_bytes(512//8,"big"))
