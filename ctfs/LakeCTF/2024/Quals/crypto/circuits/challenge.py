from Crypto.Random import random
import os
B = 12
def and_gate(a, b):
    return a & b
def or_gate(a, b):
    return a | b
def xor_gate(a, b):
    return a ^ b
def not_gate(a, x):
    return ~a & 1

def rand_circuit(size: int, input_size: int, output_size):
    circ_gates = [or_gate, not_gate, xor_gate, and_gate]
    assert size > 0 and input_size > 0 and output_size > 0
    assert output_size + size <= input_size and (input_size - output_size) % size == 0
    dec = (input_size - output_size) // size
    gates = []
    for iteration in range(1, size + 1):
        gate_level = []
        c_size = input_size - dec * iteration
        for i in range(c_size):
            gate_level.append(
                (random.choice(circ_gates),
                 (i,
                  random.randint(0, c_size + dec - 1))))
        gates.append(gate_level)
    return gates


def eval_circuit(gates, inp):
    assert len(gates) >= 1
    for level in gates:
        new_inp = []
        for gate, (i1, i2) in level:
            new_inp.append(gate(inp[i1], inp[i2]))
        inp = new_inp
    return inp


def i2b(i):
    return list(map(int, bin(i)[2:].zfill(B)))


def b2i(b):
    return int(''.join(map(str, b)), 2)

SIZE = int(input("What circuit size are you interested in ?"))
assert 3 <= SIZE <= B - 1
correct = 0
b = random.getrandbits(1)
p = rand_circuit(SIZE, B, B - SIZE)
keys = set()
while correct < 32:
    input_func = random.getrandbits(B)
    choice = int(input(f"[1] check bit\n[2] test input\n"))
    if choice == 1:
        assert int(input("bit: ")) == b
        b = random.getrandbits(1)
        p = rand_circuit(SIZE, B, B - SIZE)
        keys = set()
        correct += 1
    else:
        i = int(input(f"input: "))
        if i in keys or len(keys) > 7 or not 0 <= i <= 2 ** B:
            print("uh uh no cheating")
            exit()
        keys.add(i)
        if b == 0:
            res = random.getrandbits(B - SIZE)
        else:
            res = b2i(eval_circuit(p, i2b(i)))

        print(f"res = {res}")
print("well done !!")
print(os.getenv("flag",b"EPFL{fake_flag}"))
