import random   # TODO: heard that this is unsafe but nvm
from Crypto.Util.number import getPrime, bytes_to_long

flag = bytes_to_long(open("flag.txt", "rb").read())
p = getPrime(256)
assert flag < p
l = 32

def share_mixer(xs):
    cs = [random.randint(1, p - 1) for _ in range(l - 1)]
    cs.append(flag)
    
    # mixy mix
    random.shuffle(xs)
    random.shuffle(cs)

    shares = [sum((c * pow(x, i, p)) % p for i, c in enumerate(cs)) % p for x in xs]
    return shares


if __name__ == "__main__":
    try:
        print(f"{p = }")
        queries = input("Gib me the queries: ")
        xs = list(map(lambda x: int(x) % p, queries.split()))

        if 0 in xs or len(xs) > 32:
            print("GUH")
            exit(1)

        shares = share_mixer(xs)
        print(f"{shares = }")
    except:
        exit(1)