#!/usr/bin/env python3

import secret


def check_input(arr):
    for x in arr:
        assert 1 <= x <= int(1e9)


def check_output(arr, ans):
    ans.sort()
    for i in range(len(ans) - 1):
        assert arr[ans[i]] < arr[ans[i + 1]]


def main():
    tcs = []

    tcs.append(secret.gen(int(9e4), int(1e5)))
    for _ in range(100):
        tcs.append(secret.gen(1, 1000))

    print(len(tcs))

    for arr in tcs:
        print(*arr)

    for arr in tcs:
        check_input(arr)

        my_ans = secret.solve(arr)
        your_ans = list(map(int, input().split()))

        check_output(arr, my_ans)
        check_output(arr, your_ans)

        if len(your_ans) < len(my_ans):
            print("get better lol, maybe worship larry more?")
            exit(1)

    print("Good job! Remember to orz larry. Here's your flag", open("flag.txt", "r").read())


if __name__ == "__main__":
    main()
