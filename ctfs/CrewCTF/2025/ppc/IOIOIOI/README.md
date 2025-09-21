simple counting challenge in mod 998244353

author: hiikunZ


# IOIOIOI
## Statement
Let's think about length N binary string consisting only of the characters I and O.

The score of a string is defined as the sum of:
    - the number of contiguous substrings equal to "IOI"
    - the number of contiguous substrings equal to "IOIOI"
    - the number of contiguous substrings equal to "IOIOIOI"
and so on.

ex. score("IOIOIO") = 2 ("IOI") + 1 ("IOIOI") = 3

Find the number, modulo 998244353, of such strings have a score exactly equal to K.

## Constraints
- 1 ≦ N ≦ 10^18
- 0 ≦ K ≦ 1000

## Samples
### sample 1
#### input
```
N = 6
K = 3
```
#### output
```
4
```
#### explanation
There are 4 binary strings with length 6 have a score of 3: `IIOIOI`, `IOIOII`, `IOIOIO`, `OIOIOI`.

### sample 2
#### input
```
N = 9
K = 10
```
#### output
```
1
```
#### explanation
There is only 1 binary string with length 9 have a score of 10: `IOIOIOIOI`.

### sample 3
#### input
```
N = 40
K = 4
```
#### output
```
167288093
```
#### explanation
There are 144912719278 binary strings with length 40 have a score of 4, so the answer is 144912719278 mod 998244353 = 167288093.
