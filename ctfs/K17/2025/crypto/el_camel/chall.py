from secrets import randbelow
from sympy import isprime

def findGenerator():
    while True:
        h = randbelow(p)
        if pow(h, q, p) != 1:
            continue

        g = pow(h, 2, p)
        if g != 1:
            return g

def rng(key):
    r = randbelow(p)
    
    c = pow(g, r * x, p)
    c += key

    return c % p

if __name__ == "__main__":
    from secret import FLAG, p, q

    assert isprime(p) and isprime(q)

    g = findGenerator()
    x = randbelow(q)

    print(f"""The Mystical El-Camel is in town!
Beat their game to win a special prize...

{p}
{q}
""")

    m0 = int(input("How tall do you want the coin to be?> "))
    m1 = int(input("How long do you want the coin to be?> "))

    m = [m0, m1]
    score = 0
    symbols_to_index = {'H': 0, 'T': 1}

    for _ in range(50):
        i = randbelow(2)
        c = rng(m[i])
        print(c)

        print("The coin has been tossed...")
        guess = input("Heads or Tails! (H or T)> ")
        guess = symbols_to_index.get(guess.upper())

        if guess == i:
            print("That's correct!\n")
            score += 1
        else:
            print("Incorrect!\n")
    
    if score > 37:
        print("ElCamel is impressed! Here is your prize...")
        print(FLAG)
    else:
        print("Better luck next time!")
