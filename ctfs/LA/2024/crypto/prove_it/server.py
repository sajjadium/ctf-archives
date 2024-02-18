#!/usr/local/bin/python
import random

flag = "lactf{??????????}"
p = 171687271187362402858253153317226779412519708415758861260173615154794651529095285554559087769129718750696204276854381696836947720354758929262422945910586370154930700427498878225153794722572909742395687687136063410003254320613429926120729809300639276228416026933793038009939497928563523775713932771366072739767


if __name__ == "__main__":
    
    s = random.getrandbits(128)
    alpha = random.getrandbits(40)
    g = redacted
    ss = [pow(g, s**i, p) for i in range(1,8)]
    alphas = [pow(g, alpha * s**i, p) for i in range(1,8)]
    print(f"Use these values to evaluate your polynomials on s")
    print(f"Powers of s: {ss}")
    print(f"Powers of alpha*s: {alphas}")
    tries = 0
    while True:
        if tries >= 2:
            print("Fool me once shame on you, fool me twice shame on me")
            break
        print("Can you prove to me you know the polynomial f that im thinking of?")
        target = []
        for i in range(8):
            target.append(random.randrange(p))
        print(f"Coefficients of target polynomial: {target}")
        ts = sum([(pow(s,7 - i, p) * target[i]) % p for i in range(len(target))]) % p
        f = int(input("give me your evaluation of f(s) > ")) % p
        h = int(input("give me your evaluation of h(s) > ")) % p
        fa = int(input("give me your evaluation of f(alpha * s) > ")) % p
        if f <= 1 or h <= 1 or fa <=1 or f == p-1 or h == p-1 or fa == p-1:
            print("nope")
            exit()
            
        if pow(f, alpha, p) != fa or f != pow(h, ts, p):
            print(f"failed! The target was {ts}")
            tries += 1
            continue

        print(f"you made it! here you got {flag}")
        break


