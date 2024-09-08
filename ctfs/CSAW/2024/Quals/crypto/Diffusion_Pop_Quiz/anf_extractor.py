# To ensure correctly formatted answers for the challenge, use 1-indexed values for the output bits.
# For example, if you have an S-Box of 8 bits to 8 bits, the first output bit is 1, the second is 2, and so forth.
# Your ANF expression will have the variables y1, y2, ..., y8.

# Put your S-Boxes here.

example = [1, 0, 0, 0, 1, 1, 1, 0]

# 3 input bits: 000, 001, 010, 011, 100, 101, 110, 111
# Array indexes: 0    1    2    3    4    5    6    7
# f(x1,x2,x3):   0    1    0    0    0    1    1    1

# Customize the following settings to extract specific bits of specific S-Boxes and have a comfortable visualization of terms.

SYMBOL = 'x'
INPUT_BITS = 3
OUTPUT_BITS = 1
SBOX = example
BIT = 1

# Ignore the functions, we've implemented this for you to save your time.
# Don't touch it, it might break and we don't want that, right? ;)

def get_sbox_result(input_int):
    return SBOX[input_int]

def get_term(binary_string):
    term = ""
    i = 1
    for (count,bit) in enumerate(binary_string):
        if bit == "1":
            term += SYMBOL+str(i)+"*"
        i += 1

    if term == "":
        return "1"

    return term[:-1]

def get_poly(inputs, outputs):
    poly = ""
    for v in inputs:
        if outputs[v]:
            poly += get_term(v) + "+"
    return poly[:-1]

def should_sum(u, v, n):
    for i in range(n):
        if u[i] > v[i]:
            return False

    return True

def get_as(vs, f, n):
    a = {}
    for v in vs:
        a[v] = 0
        for u in vs:
            if should_sum(u, v, n):
                a[v] ^= f[u]

    return a

def get_anf(vs, f, n):
    return get_poly(vs, get_as(vs, f, n))

def get_vs_and_fis_from_sbox(which_fi):
    vs = []
    fis = {}
    for input_integer in range(2**INPUT_BITS):
        sbox_output = get_sbox_result(input_integer)
        input_integer_binary = bin(input_integer)[2:].zfill(INPUT_BITS)
        fis[input_integer_binary] = 0
        sbox_output_binary = bin(sbox_output)[2:].zfill(OUTPUT_BITS)

        vs.append(input_integer_binary)
        fis[input_integer_binary] = int(sbox_output_binary[which_fi-1])

    return vs, fis

def get_anf_from_sbox_fi(which_fi):
    vs, fis = get_vs_and_fis_from_sbox(which_fi)
    poly = get_anf(vs, fis, INPUT_BITS)
    return poly

output = get_anf_from_sbox_fi(BIT)
print(output)
