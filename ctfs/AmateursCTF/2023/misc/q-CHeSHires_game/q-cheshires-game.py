#!/usr/local/bin/python
from base64 import b64decode
from tqdm import tqdm
from random import randint, shuffle
from qiskit import QuantumCircuit, Aer, transpile
backend = Aer.get_backend('qasm_simulator')
import sys

def simulate_round(alice_strategy, bob_strategy):
    qc = QuantumCircuit(2, 1)
    qc.h(0)
    qc.cx(0, 1)
    qc.barrier()

    # shuffle the strategies so that the players don't get to decide who goes first
    strategies = [alice_strategy, bob_strategy]
    shuffle(strategies)

    for gate in strategies[0]:
        qc.append(gate, range(2))

    for gate in strategies[1]:
        qc.append(gate, range(2))

    qc.measure_all()

    try:
        qc = transpile(qc, backend)
        res = backend.run(qc, shots=1, memory=True).result().get_memory()[0]
        a, b = res[0], res[1]
    except Exception as e:
        print("Error running your circuit!")
        print(e)
        exit(0)

    return a, b


def run_rounds(alice_strategies, bob_strategies, rounds=1000):
    wins = 0

    for _ in tqdm(range(rounds), file=sys.stdout):
        x, y = (randint(0, 1) for _ in range(2))
        alice_strategy = alice_strategies[x]
        bob_strategy = bob_strategies[y]

        a, b = simulate_round(alice_strategy, bob_strategy)
        if (a != b) == (x & y):
            wins += 1

    return wins / rounds


def get_circuit(name, bit, value):
    print(f"Enter in your {name} strategy for {bit} = {value} as an OpenQASM file: ", end="")
    qasm_str = input()

    try:
        qasm_str = b64decode(qasm_str).decode()
    except:
        print("Error decoding base64!")
        exit(0)

    if "reset" in qasm_str:
        print("Leave those qubits alone!")
        exit(0)

    try:
        circuit = QuantumCircuit.from_qasm_str(qasm_str)
        circuit.remove_final_measurements(inplace=True)
    except:
        # thanks uiuctf orgs
        print("Error processing OpenQASM file! Try decomposing your circuit into basis gates using `transpile`.")
        exit(0)

    if circuit.num_qubits != 2:
        print("Your circuit must have exactly two qubits!")
        exit(0)

    return circuit


TARGET = 0.875 # I want you to be BETTER than optimal ;)

def main():
    print(f"Welcome to Cheshire's Quantum Game. You'll play as both Alice and Bob, and your goal is to win at least {TARGET * 100}% of the time.")
    print()
    print("This game as presented to two players, Alice and Bob, who each return a single bit after being asked a \'question\', which is a single bit as well.")
    print("To win, Alice and Bob must return bits a and b such that a XOR b == x AND y, where x and y are the bits they are given.")
    print("Alice only sees x, and Bob only sees y, and neither can communicate with each other.")
    print("In this simulation you'll be playing as both Alice and Bob.")
    print("Not to worry though, I've given you a free entangled qubit to be nice!")
    print("-" * 72)

    alice_strategies = [get_circuit("Alice", "x", i) for i in range(2)]
    bob_strategies = [get_circuit("Bob", "y", i) for i in range(2)]

    win_rate = run_rounds(alice_strategies, bob_strategies)
    if win_rate >= TARGET:
        print(
            f"Congratulations! You won {win_rate * 100}% of the time, which is greater than {TARGET * 100}%!")
        print("Here's your flag:")
        print(open("flag.txt").read())
    else:
        print(
            f"Sorry, you only won {win_rate * 100}% of the time, which is less than {TARGET * 100}%.")


if __name__ == "__main__":
    main()
