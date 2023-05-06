import gmpy2
import secrets as s
from flag import flag

fn = open(r"firstnames.py", 'r')
ln = open(r"lastnames.py", 'r')
fp = open (r"primes.py", 'r')
fn_content = fn.readlines()
ln_content = ln.readlines()
prime_arr = fp.readlines()

class RNG:
    def __init__ (self, seed, a, b, p):
        self.seed = seed
        self.a = a
        self.b = b
        self.p = p

    def gen(self):
        out = self.seed
        while True:
            out = (self.a * out + self.b) % self.p
            self.a += 1
            self.b += 1
            self.p += 1
            yield out

def getPrime ():
    prime = int(prime_arr[next(gen)].strip())
    return prime

def generate_keys():
    p = getPrime()
    q = getPrime()
    n = p*q
    g = n+1
    l = (p-1)*(q-1)
    mu = gmpy2.invert(((p-1)*(q-1)), n)
    return (n, g, l, mu)

def pallier_encrypt(key, msg, rand):
    n_sqr = key[0]**2
    return (pow(key[1], msg, n_sqr)*pow(rand, key[0], n_sqr) ) % n_sqr

N=(min(len(fn_content), len(ln_content)))
seed, a, b = s.randbelow(N), s.randbelow(N), s.randbelow(N)
lcg = RNG(seed, a, b, N)
gen=lcg.gen()

for i in range (0, 10):
    if i==0:
        name1 = fn_content[a].strip()+" "+ln_content[b].strip()
    else:
        name1 = fn_content[next(gen)].strip()+" "+ln_content[next(gen)].strip()
    name2 = fn_content[next(gen)].strip()+" "+ln_content[next(gen)].strip()
    print (f"{name1}	vs	{name2}")
    
    winner=next(gen)%2
    inp = int(input ("Choose the winner: 1 or 2\n"))
    if (winner!=inp%2):
        print ("Sorry, you lost :(")
        break
    else:
        if (i<9):
            print ("That's correct, here is the next round\n")
        else:
            print ("Congratulations! you made it")
            print ("Can you decode this secret message?")
            key=generate_keys()
            print(pallier_encrypt(key, int.from_bytes(flag, "big"), next(gen)))
















