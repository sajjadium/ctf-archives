#!/usr/local/bin/python
from random import *
from flag import flag

t = 20

print(t)

min_n = 100

for _ in range(t):
  n = randint(min_n, min_n * 2)
  print(n)
  a = []
  for i in range(n):
    a.append(i + 1)
  shuffle(a)
  for i in range(n):
    print(a[i], end="")
    if i < n - 1:
      print(" ", end="")
  print()
  arr = []
  for i in range(n):
    ar = input().split(" ")
    for j in range(n):
      ar[j] = int(ar[j])
    arr.append(ar)
  for i in range(n):
    if arr[i][a[i] - 1] != i + 1:
      print("WA")
      exit()
  for i in range(n):
    rw = []
    cl = []
    for j in range(n):
      if min(arr[i][j], arr[j][i]) < 1 or max(arr[i][j], arr[j][i]) > n:
        print("WA")
        exit()
      if arr[i][j] not in rw:
        rw.append(arr[i][j])
      if arr[j][i] not in cl:
        cl.append(arr[j][i])
    if len(rw) < n or len(cl) < n:
      print("WA")
      exit()

print("AC", flag)
