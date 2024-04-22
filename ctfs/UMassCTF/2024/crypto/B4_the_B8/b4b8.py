import random
import os
import numpy as np
from Crypto.Cipher import AES

ket_0 = np.matrix([1, 0])
ket_1 = np.matrix([0, 1])
ket_plus = (ket_0 + ket_1) / (2 ** (1 / 2))
ket_minus = (ket_0 - ket_1) / (2 ** (1 / 2))


def input_matrix(n):
    mat = []
    for i in range(n):
        row = []
        for j in range(n):
            row.append(complex(input(f"row {i}, col {j}:")))
        mat.append(row)
    m = np.matrix(mat)
    return m


qubit_id = 0


class QubitPair:
    def __init__(self, density_matrix: np.matrix):
        global qubit_id
        self.density_matrix = density_matrix
        self.id = qubit_id
        qubit_id += 1

    def measure_first(self, POVM: list[np.matrix]):
        post_measure = [np.kron(kraus, np.identity(2)) * self.density_matrix * np.kron(kraus.H, np.identity(2)) for
                        kraus in POVM]
        prob = [np.abs(np.trace(m)) for m in post_measure]
        result = random.choices([x for x in range(len(POVM))], weights=prob)
        self.density_matrix = post_measure[result[0]] / prob[result[0]]
        return result[0]

    def measure_second(self, POVM: list[np.matrix]):
        post_measure = [np.kron(np.identity(2), kraus) * self.density_matrix * np.kron(np.identity(2), kraus.H) for
                        kraus in POVM]
        prob = [np.abs(np.trace(m)) for m in post_measure]
        result = random.choices([x for x in range(len(POVM))], weights=prob)
        self.density_matrix = post_measure[result[0]] / prob[result[0]]
        return result[0]


def bell_state():
    return QubitPair(np.matrix([[1 / 2, 0, 0, 1 / 2], [0] * 4, [0] * 4, [1 / 2, 0, 0, 1 / 2]]))


def standard_basis():
    return [ket_0.H * ket_0, ket_1.H * ket_1]


def hadamard_basis():
    return [ket_plus.H * ket_plus, ket_minus.H * ket_minus]


def check_valid(a, tol=1e-8):
    eigen = np.linalg.eig(a)[0]
    return np.all(np.abs(a - a.H) < tol) and np.all(np.abs(eigen - np.abs(eigen)) < tol) and np.abs(
        np.trace(a) - 1) < tol


n = 1024

Alice_bits = [(bell_state(), 1) for s in range(n)]
Your_bits = [(x, 2) for x, _ in Alice_bits]
Bob_bits = []

key_exchanged = False


def measures(bit_list, basis_indices):
    result = 0
    POVMs = [standard_basis(), hadamard_basis()]
    for i in range(n):
        basis = (basis_indices >> i) & 1
        s, bit_num = bit_list[i]
        if bit_num == 1:
            result |= s.measure_first(POVMs[basis]) << i
        else:
            result |= s.measure_second(POVMs[basis]) << i
    return result


def randomness_test(bitstring, n=16):
    bitmat = [(bitstring >> (i * n)) & ~(-1 << n) for i in range(n)]
    for i in range(n):
        m = max(bitmat[i:])
        index = bitmat.index(m)
        bitmat[index] = bitmat[i]
        bitmat[i] = m
        if ((bitmat[i] >> (n - 1 - i)) & 1) == 0:
            continue
        for j in range(i + 1, n):
            if (bitmat[i] & bitmat[j]) >> (n - 1 - i) != 0:
                bitmat[j] ^= bitmat[i]
    return sum([1 if x == 0 else 0 for x in bitmat]) < 3


with open("flag.txt", "rb") as f:
    FLAG = f.read()

while True:
    if not key_exchanged and len(Bob_bits) == n:
        print("Bob: I've received enough states!")
        print("Alice: ok let's start then.")
        key_exchanged = True
        Alice_basis = int.from_bytes(os.urandom(n // 8), byteorder='big')
        Alice_results = measures(Alice_bits, Alice_basis)
        print("Alice: i've made my measurements.")

        Bob_basis = int.from_bytes(os.urandom(n // 8), byteorder='big')
        Bob_results = measures(Bob_bits, Bob_basis)
        print("Bob: Same here!")
        Bob_standard = ""
        Bob_hadamard = ""
        for i in range(n):
            if ((Bob_basis >> i) & 1) == 0:
                Bob_standard = Bob_standard + str((Bob_results >> i) & 1)
            else:
                Bob_hadamard = Bob_hadamard + str((Bob_results >> i) & 1)
        if randomness_test(int(Bob_hadamard, 2)) and randomness_test(int(Bob_standard, 2)):
            print("Bob: Mine passed the randomness test, looks like everything is good!")
        else:
            raise ValueError("Bob: Mine doesn't seem that random, maybe Eve's here again...")

        print(f"Bob: My bases were {('0' * n + bin(Bob_basis)[2:])[-n:]}")
        print(f"Alice: cool, my bases were {('0' * n + bin(Alice_basis)[2:])[-n:]}")

        Alice_key = ""
        Bob_key = ""
        count = 0
        for i in range(n):
            if ((Alice_basis >> i) & 1) == ((Bob_basis >> i) & 1):
                Alice_key = Alice_key + str((Alice_results >> i) & 1)
                Bob_key = Bob_key + str((Bob_results >> i) & 1)
                count += 1

        if (count - count // 10) < 128:
            raise ValueError("Bob: Hmmm, I don't think that's quite enough for us to make a key, let's start over...")

        print(
            f"Bob: Great! Now let's just make sure that our measurements actually match. My first {count // 4} bits are: {Bob_key[:count // 4]}")

        if sum([1 if a != b else 0 for a, b in zip(Alice_key[:count // 4], Bob_key[:count // 4])]) > count // 100:
            raise ValueError("Alice: that doesn't seem to match mine, eve's dropped by again it seems.")
        else:
            print("Alice: yeah that looks good.")

        Alice_key = int(Alice_key[-128:], 2)
        Alice_AES = AES.new(Alice_key.to_bytes(length=16, byteorder='big'), mode=AES.MODE_CBC)
        Bob_key = int(Bob_key[-128:], 2)
        Bob_AES = AES.new(Bob_key.to_bytes(length=16, byteorder='big'), mode=AES.MODE_CBC)
        encrypted_once = Alice_AES.encrypt(FLAG)
        encrypted_twice = Bob_AES.encrypt(encrypted_once)
        print(Alice_AES.iv.hex())
        print(Bob_AES.iv.hex())
        print(encrypted_twice.hex())

    option = int(input(
        """\nYou can:\n1. Measure a qubit\n2. Prepare a system of 2 qubits\n3. Send Bob a qubit\n4. See qubits in storage\n"""))
    if option not in [1, 2, 3, 4]:
        raise ValueError("Nope.")
    if option == 1:
        count = int(input(
            "How many Kraus operators does your POVM have? If you just want the standard basis, put 0. If you just want the hadamard basis, put 1."))
        if count < 0:
            raise ValueError("I don't think you're gonna measure much with that...")
        elif count > 4:
            raise ValueError("Unfortunately we don't quite have the hardware for that...")
        elif count == 0:
            POVM = standard_basis()
        elif count == 1:
            POVM = hadamard_basis()
        else:
            POVM = []
            print("Input your Kraus operators: ")

            for i in range(count):
                print(f"Operator #{i}:")
                m = input_matrix(2)
                POVM.append(m)
            if not np.isclose(np.sum([kraus.H * kraus for kraus in POVM]), np.identity(2)):
                raise ValueError(
                    "That doesn't seem to be physically possible set of measurements... but raise a ticket with your input if you think the check is giving a false negative!")
        index = int(input("Which state would you like to measure?"))
        if index < 0 or index >= len(Your_bits):
            raise ValueError("That's not a valid state index!")

        state, bit_number = Your_bits[index]
        print("Making measurement...")
        if bit_number == 1:
            print(f"The measurement result is: {state.measure_first(POVM)}")
        if bit_number == 2:
            print(f"The measurement result is: {state.measure_second(POVM)}")

    if option == 2:
        if len(Your_bits) > 2 * n:
            raise ValueError("You don't have enough quantum storage for that!")
        print("Input the coefficients for the 4x4 density matrix of 2 qubits: ")
        m = input_matrix(4)
        if check_valid(m):
            state = QubitPair(m)
            Your_bits.append((state, 1))
            Your_bits.append((state, 2))
            print(f"Added 2 parts of qubit with id {state.id} into storage")
        else:
            raise ValueError(
                "That doesn't seem to be a physically possible state... but raise a ticket with your input if you think the check is giving a false negative!"
            )

    if option == 3:
        if key_exchanged:
            raise ValueError("Bob: Oh look, Eve's trying to send me qubits. That can't be good...")
        index = int(input("Which bits would you like to send to Bob?"))
        if index < 0 or index >= len(Your_bits):
            raise ValueError("That's not a valid state index!")
        Bob_bits.append(Your_bits.pop(index))

    if option == 4:
        for i, t in enumerate(Your_bits):
            print(f"#{i} | id: #{t[0].id}, part of qubit: {t[1]}")
