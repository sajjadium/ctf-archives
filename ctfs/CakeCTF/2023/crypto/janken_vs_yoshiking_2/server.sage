import random
import signal
import os

HANDNAMES = {
    1: "Rock",
    2: "Scissors",
    3: "Paper"
}

def commit(M, m):
    while True:
        r = random.randint(2, 2**256)
        if r % 3 + 1 == m:
            break
    return M**r, r


signal.alarm(1000)

flag = os.environ.get("FLAG", "neko{old_yoshiking_never_die,simply_fade_away}")
p = 1719620105458406433483340568317543019584575635895742560438771105058321655238562613083979651479555788009994557822024565226932906295208262756822275663694111
M = random_matrix(GF(p), 5)
print("[yoshiking]: Hello! Let's play Janken(RPS)")
print("[yoshiking]: Here is p: {}, and M: {}".format(p, M.list()))

round = 0
wins = 0
while True:
    round += 1
    print("[system]: ROUND {}".format(round))

    yoshiking_hand = random.randint(1, 3)
    C, r = commit(M, yoshiking_hand)
    print("[yoshiking]: my commitment is={}".format(C.list()))

    hand = input("[system]: your hand(1-3): ")
    print("")
    try:
        hand = int(hand)
        if not (1 <= hand <= 3):
            raise ValueError()
    except ValueError:
        print("[yoshiking]: Ohhhhhhhhhhhhhhhh no! :(")
        exit()

    print("[yoshiking]: My hand is ... {}".format(HANDNAMES[yoshiking_hand]))
    print("[yoshiking]: Your hand is ... {}".format(HANDNAMES[hand]))
    result = (yoshiking_hand - hand + 3) % 3
    if result == 0:
        print("[yoshiking]: Draw, draw, draw!!!")
        print("[yoshiking]: I'm only respect to win!")
        print("[system]: you can check that yoshiking doesn't cheat")
        print("[system]: here's the secret value: {}".format(r))
        exit()
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
        print("[system]: here's the secret value: {}".format(r))
        exit()

print("[yoshiking]: Wow! You are the king of roshambo!")
print("[yoshiking]: suge- flag ageru")
print(flag)
