from solver import Solve
import signal
import secrets


def TLE(signum, frame):
    print("Time Limit Exceeded. Try again...")
    exit(0)


signal.signal(signal.SIGALRM, TLE)
signal.alarm(300)

params = [  # (N_min, N_max, K_min, K_max)
    (1, 15, 0, 15),  # Test 1
    (1, 1000, 0, 1000),  # Test 2
    (5 * 10**8, 10**9, 0, 1000),  # Test 3
    (5 * 10**17, 10**18, 900, 1000),  # Test 4
]

T = 300

for i in range(T):
    test_id = i // 75
    N_min, N_max, K_min, K_max = params[test_id]
    N = N_min + secrets.randbelow(N_max - N_min + 1)
    K = K_min + secrets.randbelow(K_max - K_min + 1)

    ans = Solve(N, K)
    assert 0 <= ans < 998244353

    print("Test", i + 1)
    print(f"{N = }")
    print(f"{K = }")
    print("Your answer: ", end="")
    player_ans = int(input())

    if ans == player_ans:
        print("Accepted!")
    else:
        print("Wrong Answer. Try again...")
        exit(0)

print("Congratulations! Here is your flag:")
print(open("flag.txt", "r").read())
