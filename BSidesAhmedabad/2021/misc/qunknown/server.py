import os
import numpy
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import *

def challenge():
    # Create a random gate
    dx, dy, dz = [numpy.random.rand()*numpy.pi] * 3
    def U(index):
        return merge(merge(RX(index, dx), RY(index, dy)), RZ(index, dz))
    def Udag(index):
        return merge(merge(RZ(index, -dz), RY(index, -dy)), RX(index, -dx))

    GATES = {
        'CNOT': (CNOT, 2),
        'H': (H, 1), 'X': (X, 1), 'Y': (Y, 1), 'Z': (Z, 1),
        'S': (S, 1), 'SDAG': (Sdag, 1), 'T': (T, 1), 'TDAG': (Tdag, 1),
        'U': (U, 1), 'UDAG': (Udag, 1)
    }
    CONSUMED = set() # We don't have enough resources :(

    def assemble_circuit(asm, qbits=2):
        """ Convert assembly into quantum circuit
        i.e.  q0 ---+--[Z]--
                    |        <= "CNOT 0,1; Z 0; H 1;"
              q1 --[X]-[H]--
        """

        class QasmException(Exception):
            pass

        def apply(gate, args):
            return gate(*args)

        circuit = QuantumCircuit(qbits)
        cnt = 0
        for instruction in asm.replace('\n', '').split(';'):
            t = instruction.strip().split()
            if t == []:
                continue

            if len(t) < 2:
                raise QasmException("Invalid instruction")

            opecode, operand = t[0].upper(), t[1:]
            if opecode not in GATES:
                raise QasmException("Invalid gate")

            if opecode in CONSUMED:
                raise QasmException("Lack of gate")

            operand = list(map(lambda x: int(x), ''.join(t[1:]).split(',')))
            if not all(map(lambda x: 0 <= x < qbits, operand)):
                raise QasmException("Invalid quantum bit specified")

            if GATES[opecode][1] != len(operand):
                raise QasmException("Invalid number of operands")

            CONSUMED.add(opecode)
            gate = apply(GATES[opecode][0], operand)
            circuit.add_gate(gate)

            cnt += 1
            if cnt > 100:
                raise QasmException("Too large circuit")

        return circuit

    # 2-bit quantum state
    state = QuantumState(2)
    state.set_zero_state()

    # Randomize 1st qubit (|0>|0> --> |phi>|0>)
    RX(0, numpy.random.rand()*numpy.pi).update_quantum_state(state)
    RY(0, numpy.random.rand()*numpy.pi).update_quantum_state(state)
    RZ(0, numpy.random.rand()*numpy.pi).update_quantum_state(state)
    answer_state = state.copy()

    # Apply U gate to 1st qubit (answer_state)
    U(0).update_quantum_state(answer_state)

    # p0 is the probability that 1st qubit is measured to be 0
    p0 = answer_state.get_marginal_probability([0, 2])

    # Execute your pre-processor (state)
    # You can change the state before measurement
    asm = input("Pre-processor: ")
    circ_pre = assemble_circuit(asm)
    circ_pre.update_quantum_state(state)

    # Apply U gate to 2nd qubit (state)
    U(1).update_quantum_state(state)

    # Measure and destroy 1st qubit (state)
    Measurement(0, 0).update_quantum_state(state)
    print("Measure: " + str(state.get_classical_value(0)))

    # Execute your post-processor (state)
    # Your goal is to create U|phi> after you measure |phi>
    asm = input("Post-processor: ")
    circ_post = assemble_circuit(asm)
    circ_post.update_quantum_state(state)

    # p1 is the probability that 2nd qubit is measured to be 0
    p1 = state.get_marginal_probability([2, 0])

    # Is 2nd qubit U|phi>?
    assert numpy.isclose(p0, p1)

if __name__ == '__main__':
    for rnd in range(1, 11):
        print(f"[ROUND {rnd}/10]")
        try:
            challenge()
            print("[+] Success!!!")
        except Exception as e:
            print("[-] Failure...")
            print(f"    {e}")
            break
    else:
        print(os.getenv("FLAG", "Fake{sample_flag}"))
