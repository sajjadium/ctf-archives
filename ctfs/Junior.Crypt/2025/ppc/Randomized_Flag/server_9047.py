from random import  getrandbits

with open("flag.txt","rb") as f:
    flag = f.read()

for i in range(2**64):
    print(getrandbits(32) + flag[getrandbits(32) % len(flag)])
    a = input()  # 1 - I known flag, else - next number
    if a == '1':
        ans = input('Flag is: ')
        if ans == flag.decode():
            print (f"Your flag: {flag}")
            break