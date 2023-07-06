#!/usr/bin/env python3

from os import system
from base64 import b64decode
import numpy as np

from qiskit import QuantumCircuit
import qiskit.quantum_info as qi
from qiskit.circuit.library import StatePreparation

WIRES = 5


def normalization(msg):
    assert(len(msg) <= WIRES**2)
    state = np.array([ord(c) for c in msg.ljust(2**WIRES, ' ')])
    norm = np.linalg.norm(state)
    state = state / norm
    return (state, norm)

def transform(sv, n):
    legal = lambda c: ord(' ') <= c and c <= ord('~')
    renormalized = [float(i.real)*n for i in sv]
    rn_rounded = [round(i) for i in renormalized]
    if not np.allclose(renormalized, rn_rounded, rtol=0, atol=1e-2):
        print("Your rehydrated statevector isn't very precise. Try adding at least 6 decimal places of precision, or contact the challenge author if you think this is a mistake.")
        print(rn_rounded)
        exit(0)
    if np.any([not legal(c) for c in rn_rounded]):
        print("Invalid ASCII characters.")
        exit(0)
    return ''.join([chr(n) for n in rn_rounded])

def make_circ(sv, circ):
    qc = QuantumCircuit(WIRES)
    qc.append(circ.to_instruction(), range(WIRES))
    sp = QuantumCircuit(WIRES, name="echo 'Hello, world!'")
    sp.append(StatePreparation(sv), range(WIRES))
    qc.append(sp.to_instruction(), range(WIRES))
    return qc

def print_given(sv, n):
    placeholder = QuantumCircuit(WIRES, name="Your Circ Here")
    placeholder.i(0)

    circ = make_circ(sv, placeholder)
    print(circ.draw(style={
        "displaytext": {
            "state_preparation": "<>"
            }
        }))
    new_sv = qi.Statevector.from_instruction(circ)
    print(f'Normalization constant: {n}')
    print("\nExecuting...\n")
    system(transform(new_sv, n))

def main():
    print("Welcome to the Quantum Secure Shell. Instead of dealing with pesky encryption, just embed your commands into our quantum computer! I batched the next command in with yours, hope you're ok with that!")

    given_sv, given_n = normalization("echo 'Hello, world!'")
    print_given(given_sv, given_n)

    try:
        qasm_str = b64decode(input("\nPlease type your OpenQASM circuit as a base64 encoded string: ")).decode()
    except:
        print("Error decoding b64!")
        exit(0)
    try:
        circ = QuantumCircuit.from_qasm_str(qasm_str)
        circ.remove_final_measurements(inplace=True)
    except:
        print("Error processing OpenQASM file! Try decomposing your circuit into basis gates using `transpile`.")
        exit(0)
    if circ.num_qubits != WIRES:
        print(f"Your quantum circuit acts on {circ.num_qubits} instead of {WIRES} qubits!")
        exit(0)

    try:
        norm = float(input("Please enter your normalization constant (precision matters!): "))
    except:
        print("Error processing normalization constant!")
        exit(0)
    try:
        sv_circ = make_circ(given_sv, circ)
    except:
        print("Circuit runtime error!")
        exit(0)

    print(sv_circ.draw())
    command = transform(qi.Statevector.from_instruction(sv_circ), norm)

    print("\nExecuting...\n")
    system(command)

if __name__ == "__main__":
    main()
