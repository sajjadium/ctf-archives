from sage.all import sqrt, floor
from secret import flag

def getTriNumber(n):
    return n * (n + 1) // 2  # Ensure integer division

def pair(n1, n2):
    S = n1 + n2
    return getTriNumber(S) + n2

def pair_array(arr):
    result = []
    for i in range(0, len(arr), 2):
        result.append(pair(arr[i], arr[i + 1]))    
    return result

def pad_to_power_of_two(arr):
    result = arr
    n = len(result)
    while (n & (n - 1)) != 0:
        result.append(0)
        n += 1
    return result
    
flag = [ord(f) for f in flag]  
flag = pad_to_power_of_two(flag)

temp = flag
for i in range(6):
    temp = pair_array(temp)

print("Encoded:", temp)
