from struct import pack
import random, time

def bytes2matrix(b):
	return [list(map(lambda x : x, list(b[i:i+4]))) for i in range(0, len(b), 4)]

def matrix2bytes(m):
	return b''.join(map(lambda x : b''.join(map(lambda y : pack('!H', y), x)), m))

def multiply(A,B):
	C = [[0 for i in range(4)] for j in range(4)]
	for i in range(4):
		for j in range(4):
			for k in range(4):
				C[i][j] += A[i][k] * B[k][j]
	return C


def main():
	random.seed(time.time())
	key = [[random.randint(0,64) for i in range(4)] for j in range(4)]

	data = open("flag.png", "rb").read()
	out = open("flag.png.enc", 'wb')
	
	for i in range(0, len(data), 16):
		cipher = multiply(bytes2matrix(data[i:i+16]), key)
		out.write(matrix2bytes(cipher))
	out.close()

if __name__ == '__main__':
    main()