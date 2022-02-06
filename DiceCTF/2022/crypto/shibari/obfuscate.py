"""
if you can't get the python module to work,
this script is basically equivalent to the C++ file 
crag-python/BraidGroup/main/ireland.cpp
"""

# https://github.com/the-entire-country-of-ireland/crag-python
import fast_braids

def load_braid(filename):
	with open(filename, "r") as f:
		data = f.read()
	data = data.strip(" ")
	data = data.split(" ")
	data = [int(i) for i in data]
	return fast_braids.createBraid(data)

def save_braid(braid, filename):
	res = braid.toVector()
	with open(filename, "w") as f:
		r = [str(i) for i in res]
		s = " ".join(r)
		f.write(s)

def save_LNF(LNF, filename):
	e = LNF.getHalfTwistExponent()
	Ps = LNF.getPermutations()
	with open(filename, "w") as f:
		s = repr((e, Ps))
		f.write(s)

N = 136

def process(i):
	print("")
	print(i)
	fn_base = f"{i}.txt"
	braid = load_braid("raw_braids/" + fn_base)

	LNF = fast_braids.LNF(braid, N)
	print("computed LNF")

	obf_braid = LNF.getBraid()
	save_braid(obf_braid, "obfuscated_braids/" + fn_base)
	print("computed obfuscated braid")

for i in range(6):
	process(i)
