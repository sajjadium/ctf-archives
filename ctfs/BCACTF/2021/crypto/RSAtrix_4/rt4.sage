import binascii

n = 12250029783200708035442688430907155767407534107589849686856901602023044745588908817287475893837114530200770756874643028769505799000457410384361237849623138499604018042429324632369604169982302200676229
e = 3
d = 8166686522133805356961792287271437178271689405059899791237934401348696497059272544858317262558076346381188965364240700913300230902627376039004235148937938590077100058175744322454350852499041154941427
N = 62

R = Zmod(n)
MS = MatrixSpace(R, N, N)
G = SECRET # G is a server-side secret!

def encrypt(m):
	M = m * G
	return (M^e).list()

with open("flag.txt", "r") as f:
    flag = f.read().strip().encode("ascii")
m = int(binascii.hexlify(flag), 16)

mats = {"I": MS.identity_matrix(), "G": G, "E": MS(encrypt(m))}

print("""
Welcome to the *advanced* RSAtrix demo calculator! 
Here, you can define matrix variables in terms of sums, products, or powers of matrices.
You can also multiply a matrix by a constant.
There's only one catch: you can only receive the trace of the resulting matrices!
""")

while True:
	print("Would you like to print the traces of your stored matrices (P), add two matrices (A), \nmultiply two matrices (M), multiply a matrix by a constant (C), take a matrix power (X), or quit (Q)?")
	try:
		l = input(">>> ").strip().upper()
		if (len(l) > 1):
			print("You inputted more than one character...")
		elif (l == "Q"):
			print("We hope you enjoyed!")
			exit()
		elif (l == "P"):
			print("Here the traces of your matrices:")
			for k in mats:
				print(k + ": " + str(mats[k].trace()))
		elif (l == "A"):
			print("What is the name of the first matrix you would like to add?")
			A = input(">>> ").strip()
			print("What is the name of the second matrix you would like to add?")
			B = input(">>> ").strip()
			C = mats[A]+mats[B]
			print("The trace of their sum is: " + str(C.trace()))
			print("Would you like to save this matrix? (Y/N)")
			I = input(">>> ").strip().upper()
			if I == "N":
				continue
			print("What would you like the name of the matrix to be?")
			N = input(">>> ").strip()
			mats[N] = C
			print("Matrix saved.")
		elif (l == "M"):
			print("What is the name of the first matrix you would like to multiply?")
			A = input(">>> ").strip()
			print("What is the name of the second matrix you would like to multiply?")
			B = input(">>> ").strip()
			C = mats[A]*mats[B]
			print("The trace of their product is: " + str(C.trace()))
			print("Would you like to save this matrix? (Y/N)")
			I = input(">>> ").strip().upper()
			if I == "N":
				continue
			print("What would you like the name of the matrix to be?")
			N = input(">>> ").strip()
			mats[N] = C
			print("Matrix saved.")
		elif (l == "C"):
			print("What is the name of the matrix you would like to multiply?")
			A = input(">>> ").strip()
			print("What is the value of the constant you would like to multiply it by?")
			B = int(input(">>> ").strip())
			C = B * mats[A]
			print("The trace of the product is: " + str(C.trace()))
			print("Would you like to save this matrix? (Y/N)")
			I = input(">>> ").strip().upper()
			if I == "N":
				continue
			print("What would you like the name of the matrix to be?")
			N = input(">>> ").strip()
			mats[N] = C
			print("Matrix saved.")
		elif (l == "X"):
			print("What is the name of the matrix you would like to exponentiate?")
			A = input(">>> ").strip()
			print("What is the value of the exponent you would like to use?")
			B = int(input(">>> ").strip())
			C = mats[A]^B
			print("The trace of the matrix power is is: " + str(C.trace()))
			print("Would you like to save this matrix? (Y/N)")
			I = input(">>> ").strip().upper()
			if I == "N":
				continue
			print("What would you like the name of the matrix to be?")
			N = input(">>> ").strip()
			mats[N] = C
			print("Matrix saved.")
	except:
		print("Your input caused an error.")