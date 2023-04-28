import os
import signal

signal.alarm(1000)

for _ in range(77):
    x = randrange(1, 1 << 64)
    print("x:", x)
    a, b = int(input('a: ')), int(input('b: '))
    assert a != 0 and b != 0, "[kymn] Sorry for you!"

    for _ in range(10):
        p = random_prime(1 << 256)
        if legendre_symbol(x^3 + a*x + b, p) == 1:
            break
    else:
        print("[kymn] (^o^)m9 Bad luck!")
        exit()

    F = GF(p)
    E = EllipticCurve(F, [F(a), F(b)])
    G = E.lift_x(F(x))

    k = randrange(1, p)
    Q = k * G
    kymn_dice = (k % 6) + 1
    print("commitment:", (G[1], Q[1]))

    player_dice = int(input("Your dice: "))
    assert 1 <= player_dice <= 6, "Wrong input"

    if kymn_dice + player_dice == 7:
        print("[kymn] o(.o.)o You lucky bastard!")

    else:
        print("[kymn] (^o^)m9 Bad luck!")
        print("proof:", (p, k))
        exit()

else: # 77 wins!
    print("[kymn] I got totally destroyed! Hats off to you...")
    print("FLAG:", os.getenv("FLAG", "RicSec{*** REDACTED ***}"))
