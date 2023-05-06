import random
import signal
from flag import flag
from Crypto.Util.number import getStrongPrime, inverse

HANDNAMES = {
    1: "Rock",
    2: "Scissors",
    3: "Paper"
}

def commit(m, key):
    (g, p), (x, _) = key
    r = random.randint(2, p-1)
    c1 = pow(g, r, p)
    c2 = m * pow(g, r*x, p) % p
    return (c1, c2)


def decrypt(c, key):
    c1, c2 = c
    _, (x, p)= key

    m = c2 * inverse(pow(c1, x, p), p) % p
    return m


def keygen(size):
    p = getStrongPrime(size)
    g = random.randint(2, p-1)
    x = random.randint(2, p-1)

    return (g, p), (x, p)


signal.alarm(3600)
key = keygen(1024)
(g, p), _ = key
print("[yoshiking]: Hello! Let's play Janken(RPS)")
print("[yoshiking]: Here is g: {}, and p: {}".format(g, p))

round = 0
wins = 0
while True:
    round += 1
    print("[system]: ROUND {}".format(round))

    yoshiking_hand = random.randint(1, 3)
    c = commit(yoshiking_hand, key)
    print("[yoshiking]: my commitment is={}".format(c))

    hand = input("[system]: your hand(1-3): ")
    print("")
    try:
        hand = int(hand)
        if not (1 <= hand <= 3):
            raise ValueError()
    except ValueError:
        print("[yoshiking]: Ohhhhhhhhhhhhhhhh no! :(")
        exit()

    yoshiking_hand = decrypt(c, key)
    print("[yoshiking]: My hand is ... {}".format(HANDNAMES[yoshiking_hand]))
    print("[yoshiking]: Your hand is ... {}".format(HANDNAMES[hand]))
    result = (yoshiking_hand - hand + 3) % 3
    if result == 0:
        print("[yoshiking]: Draw, draw, draw!!!")
    elif result == 1:
        print("[yoshiking]: Yo! You win!!! Ho!")
        wins += 1
        print("[system]: wins: {}".format(wins))

        if wins >= 100:
            break
    elif result == 2:
        print("[yoshiking]: Ahahahaha! I'm the winnnnnnner!!!!")
        print("[yoshiking]: You, good loser!")
        print("[system]: you can check that yoshiking doesn't cheat")
        print("[system]: here's the private key: {}".format(key[1][0]))
        exit()

print("[yoshiking]: Wow! You are the king of roshambo!")
print("[yoshiking]: suge- flag ageru")
print(flag)
