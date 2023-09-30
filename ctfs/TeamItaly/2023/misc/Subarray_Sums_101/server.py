import random
import os
import signal

FLAG = os.environ.get("FLAG", "flag{test_flag}")

n = 128
secret = [random.randint(0, 1) for _ in range(n)]

queries_results = {}

for i in range(0, n):
    subarray_sum = 0
    for j in range(i+1, n+1):
        subarray_sum += secret[j-1]
        if subarray_sum in queries_results:
            queries_results[subarray_sum] += 1
        else:
            queries_results[subarray_sum] = 1

def signal_handler(signum, frame):
    print("Time is up!")
    raise TimeoutError

signal.signal(signal.SIGALRM, signal_handler)

def main():

    print(f"You have {n//2} queries to guess my secret!")

    for _ in range(n//2):
        k = int(input('> '))

        if k not in queries_results:
            print(0)
        else:
            print(queries_results[k])
    guess = input("Give me your guess: ")

    if guess == ''.join(str(x) for x in secret):
        print(FLAG)
    else:
        print("Nope")


if __name__ == '__main__':
    signal.alarm(20)
    try:
        main()
    except TimeoutError:
        exit(1)
