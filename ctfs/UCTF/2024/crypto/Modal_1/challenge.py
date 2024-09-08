from secret import flag

size = len(flag)
for i in range(size-1):
    print(ord(flag[i]) + ord(flag[i+1]), end=",")