import math
import hashlib
import sys

SIZE = int(3e5)
VERIFY_KEY = "46e1b8845b40bc9d977b8932580ae44c"


def getSequence(A, B, n, m):

    ans = [0] * (n + m - 1)

    for x in range(n):
        for y in range(m):
            ans[x + y] += A[x] * B[y]

    return ans


A = [0] * SIZE
B = [0] * SIZE

document1 = open("Document 1.txt", "r")
nums1 = document1.readlines()

idx = 0

for num in nums1:
    A[idx] = int(num.strip())
    idx += 1

document2 = open("Document 2.txt", "r")
nums2 = document2.readlines()

idx = 0

for num in nums2:
    B[idx] = int(num.strip())
    idx += 1

sequence = getSequence(A, B, SIZE, SIZE)
val = 0

for num in sequence:
    val = (val + num)

val = str(val)
val_md5 = hashlib.md5(val.encode()).hexdigest()

if val_md5 != VERIFY_KEY:
    print("Wrong solution.")
    sys.exit(1)

key = str(hashlib.sha256(val.encode()).digest())
flag = "ctf{" + "".join(list([x for x in key if x.isalpha() or x.isnumeric()])) + "}"

print(flag)