import sys, socket
from protocol import *
from player import *


DESCRIPTION = """
[Many-Time-QKD]

    # Description
    Alice and Bob are communicating through a noiseless channel, and you task is to steal their secret!

    # Hint
    When there are n qubits (quantum bits) being transmitted, you can input a string of length n.
    To observe the i-th qubit, set the i-th character to '1'.
    Otherwise, set the i-th character to '0'.
"""

def main():
    print(DESCRIPTION)
    f = open("/home/guessq/flag", "r")
    flag = f.read()
    alice = Player(msg=flag)
    bob = Player()
    qkd = QKD(alice, bob)
    qkd.run()


if __name__ == "__main__":
    main()
