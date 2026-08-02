import random;

Welcome = "The Sussy United States Secret Service (SUSSS) is very confident in our cybersecurity. You'll never get our secret!"
print(Welcome);

flag = int(open('flag.txt','rb').read().hex(),16);
n = 3;
p = int(input("Input your favorite mod: "));
assert(p * p < flag);
# Multiply matrix a and b mod p
def mul(a,b,p):
	assert len(a) == len(a[0]) and len(b) == len(b[0]) and len(a) == len(b);
	n = len(a);
	uwu = [[0 for _ in range(n)] for _ in range(n)];
	for k in range(n):
		for i in range(n):
			for j in range(n):
				uwu[i][j] += a[i][k] * b[k][j];
				uwu[i][j] %= p;

	return uwu;

# Take matrix m to the nth power mod p
def pow(m,n,p):
	if(n == 0):
		return [[(0,1)[i == j] for j in range(len(m[i]))] for i in range(len(m))];
	if(n == 1):
		return m;
	uwu = pow(m,n // 2,p);
	if(n % 2 == 1):
		return mul(mul(uwu,uwu,p),m,p);
	return mul(uwu,uwu,p);

# Make a random matrix of size n modulo p
def randomMatrix(n,p):
	uwu = [[0 for _ in range(n)] for _ in range(n)];
	for i in range(n):
		for j in range(n):
			uwu[i][j] = random.randint(0,p - 1);
	return uwu;

# Divides tot randomly into n parts
def get_partition(tot,n):
	partitions = [tot];
	for i in range(n - 1):
		partitions.append(random.randint(0,tot));
	partitions.sort()
	for i in range(n - 1,0,-1):
		partitions[i] -= partitions[i - 1];
	return partitions

# Convolute a matrix mod p with generator x
def convolute(m,x,p):
	uwu = 0;
	owo = 1;
	for i in range(len(m)):
		for j in range(len(m[i])):
			owo = (owo * x) % p;
			uwu += (owo * m[i][j]) % p;
			uwu %= p;
	return uwu;

# Apply initial noise
matrix = randomMatrix(n,p);
# Shred the secret into many parts
shreded = get_partition(flag,n);
for i in range(n):
	matrix[i][i] = shreded[i] % p;

randomPower = random.randint(10,1e18);
print("The message is powered up by " + str(randomPower));

matrix = pow(matrix,randomPower,p);

for i in range(n + 1):
	x = int(input("What is your favorite power: "));
	new_matrix = pow(matrix,x,p);
	y = int(input("What is your favorite generator: "));
	z = convolute(new_matrix,y,p);
	print("The complete mess you get after our encryption is " + str(z));