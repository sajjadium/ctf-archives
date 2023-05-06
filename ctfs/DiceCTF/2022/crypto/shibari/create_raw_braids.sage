load("braid-io.sage")

def split_string(a_string, n):
    return [a_string[index : index + n] for index in range(0, len(a_string), n)]

def toBinary(n, L):
    return ''.join(str(1 & int(n) >> i) for i in range(L))


nbits_flag = 32

##########################


n = 2 * nbits_flag
BCC = BraidCircuitCompiler(n)
braid = BCC.get_identity_gate()

b = 0
t = nbits_flag
while b < t - 1:
    print(b, b+1, t)
    braid *= BCC.get_CCX_gate(b, b+1, t)
    b += 2
    t += 1

print(t, n-1)

CX_braid = BCC.get_CX_gate(t-1, n-1)

braid = braid * CX_braid * ~braid
print("compiled!")

##########################

flag = "????????????????????????"

assert len(flag) == 24
split_flag = split_string(flag, 4)

for i,f in enumerate(split_flag):
	bin_flag = toBinary(int.from_bytes(f.encode(), "big"), nbits_flag)

	prefix = BCC.get_identity_gate()
	for j,x in enumerate(bin_flag):
	    e = (x == '0')
	    prefix *= BCC.get_X_gate(j)**e

	new_braid = prefix * braid * ~prefix

	write_braid(new_braid, f"raw_braids/{i}.txt")
	print(f"saved circuit #{i}")
