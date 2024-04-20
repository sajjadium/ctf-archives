#!/usr/bin/python3

import signal
from functools import wraps

supers3cr3t = 'NexusCTF{REDACTED}'
attempt_limit = 3
timeout_seconds = 5

def timeout_handler(signum, frame):
    print("\nTimeout reached. Exiting...")
    exit(0)

def limit_attempts(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for _ in range(attempt_limit):
            func(*args, **kwargs)
        print("Exceeded attempt limit. Exiting...")
        exit(0)
    return wrapper

@limit_attempts
def challenge():
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        inp = input("Present the Warrior's code to attain the key to victory: ")
        signal.alarm(0)
        if len(inp) < 17 and 'supers3cr3t' not in inp:
            print(eval(inp))
        else:
            print('You are still not worthy. Come back another time')
    except KeyboardInterrupt:
        print("\nAbort!!")
        exit(0)

if __name__ == "__main__":
    print("----------------Welcome to the Dragon's Lair-----------------")
    challenge()