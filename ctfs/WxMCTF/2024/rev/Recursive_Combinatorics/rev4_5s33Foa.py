from hashlib import sha512

def acid(s):
    return sha512(s.encode('utf-8')).hexdigest()

def ___(n, k):
    a = 0
    for _ in range(1, k+1):
        j = 0
        while(n>=(1<<j)):
            a += n&(1<<j)
            j += 1
    return a

def rock(a, n):
    if n == 0:
        return 1
    return a*rock(___(a, a),n>>1) if(n&1==1) else rock(___(a, a),n>>1)

def paper(n):
    x = rock(n, n)
    return {i: [(1<<i>>i)-1, 1<<i, (1<<i)<<1, ((1<<i)<<1)+(1<<i)] for i in range(x)}

def scissors(n, a, x):
	if n == 0:
		return [0]*x
	ls = [int(n%a)] + [int(n%a) for _ in range(n) if (n := n // a)]
	ls += [0]*(x-len(ls))
	return ls

def go(n):
	final, lib, x = 0, paper(n), rock(n, n)
	for i in range(1<<(x<<1)):
		ls = scissors(i, 4, x)
		tot = sum( [lib[j][ls[j]] for j in range(x)] )
		final += int(tot == n)
	return final

number = int(input("Enter your number: "))
print(go(number))