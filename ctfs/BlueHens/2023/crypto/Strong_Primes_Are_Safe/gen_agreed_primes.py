from Crypto.Util import number
import multiprocessing

COUNT = 1024
SIZE = 2048
with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
    with open("strong_primes",'w') as f:
        for p in pool.imap_unordered(number.getStrongPrime,[SIZE for _ in range(COUNT)]):
            f.write(hex(p)[2:] + '\n')
