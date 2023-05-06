#!/usr/bin/env python3

import sys
import signal
import random, string, hashlib


def proof_of_work():
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    digest = hashlib.sha256(proof.encode()).hexdigest()
    print("sha256(XXXX+%s) == %s" % (proof[4:], digest))
    x = input("Give me XXXX: ")
    if len(x)!=4 or hashlib.sha256((x+proof[4:]).encode()).hexdigest() != digest: 
        print("Sorry~ bye~")
        return False
    print("Right!")
    return True


def main():
    from backend import bet_in_casino, exchange_key
    from players import AAA, GAMBLER
    from casino import CASINO_DESCRIPTION

    print(CASINO_DESCRIPTION)
    sys.stdout.flush()
    signal.alarm(300)

    aaa = AAA()
    gambler = GAMBLER()

    network = exchange_key(aaa, gambler, 128)
    if aaa.secret_iv != gambler.secret_iv:
        print("byebye~~")
        network.stop(True)
        return
    print("good job!")

    network = bet_in_casino(network, aaa, gambler, 256)
    network.stop(True)


if __name__ == "__main__":
    if proof_of_work():
        main()
