from sympy import prevprime
from random import randint
import sys

#init

sys.setrecursionlimit(1000)

#constants

n = 100
m = prevprime(n ** (n - 2))
k = 65537
w = randint(1, n)

mx = 80 #less than log256(m)
flagkey = b"This piece of text is the flag key wow omg!"

flag = open("./flag.txt", "r").read()

#hash funcs

def hexToStr(s):
    try:
        return bytes.fromhex(s).rstrip(b'\x00')
    except:
        return ""

def strToInt(s):
    return int.from_bytes(s, "little")
    
def intHash(x):
    return pow(x, k, m)

def intToArray(x):
    a = []
    for i in range(n - 2):
        a.append(x % n)
        x //= n
    return a

def arrayToTree(a):
    d = [0] * n
    for i in a:
        d[i] += 1

    a.append(a[-1])

    j, l = 0, 0
    e = []
    for i in a:
        while d[j] != 0 or i == j:
            j += 1
        if d[l] != 0 or i == l:
            l = j
        
        e.append((i, l))

        d[i] -= 1
        d[l] -= 1

        if d[i] == 0 and i < j:
            l = i

    return e

def dfs(g, c, p):
    ret = c
    for i in g[c]:
        if i != p:
            ret = max(ret, dfs(g, i, c))

    return ret

def treeHash(e):
    g = [[] for i in range(n)]

    for i in e:
        g[i[0]].append(i[1])
        g[i[1]].append(i[0])

    ret = 1
    for i in e:
        ret *= (dfs(g, i[0], i[1]) + dfs(g, i[1], i[0]) + w)

    return ret

def H(s):
    x = strToInt(s)
    y = intHash(x)
    a = intToArray(y)
    e = arrayToTree(a)
    return treeHash(e)

#interaction

print("Welcome to my TreeHash generator.")
print(f"You can input any string of length up to {mx} chars, and I'll give you its hash!")
print("Note: trailing null bytes are stripped.\n")

print("I am testing its security, so if you can generate a collision with the flag key I'll give you the flag!")
print(f"The flag key is: {str(flagkey)[1:]}\n")

while(1):
    s = input("Input a hex encoded string: ")
    print('')

    s = hexToStr(s)

    if len(s) == 0:
        print("Invalid hex format.\n")
        continue

    if len(s) > mx:
        print("String length too large.\n")
        continue

    print(f"String {str(s)[1:]} has hash: \n{H(s)}\n")

    if s == flagkey:
        print("This is just the flag key smh.\n")
    elif H(s) != H(flagkey):
        print("The string is not a collision.\n")
    else:
        print("Wtmoo you found a collision!")
        print(f"The flag is: {flag}")
        break
