#!/usr/bin/env python3

from qiskit import QuantumCircuit
import qiskit.quantum_info as qi
from base64 import b64decode
from secret import CHORD_PROGRESSION, FLAG, LORE

QUBITS = 4

# No flat notes because they're just enharmonic to the sharps
NOTE_MAP = {
    '0000': 'C',
    '0001': 'C#',
    '0010': 'D',
    '0011': 'D#',
    '0100': 'E',
    '0101': 'F',
    '0110': 'F#',
    '0111': 'G',
    '1000': 'G#',
    '1001': 'A',
    '1010': 'A#',
    '1011': 'B',
    '1100': 'X', # misc note (aka ignore these)
    '1101': 'X',
    '1110': 'X',
    '1111': 'X',
}

# legend says that one only requires the major and minor chords to unlock the secret gates
CHORD_MAP = {
    'Cmaj' : {'C', 'E', 'G'},
    'C#maj': {'C#', 'E#', 'G#'},
    'Dmaj' : {'D', 'F#', 'A'},
    'D#maj': {'D#', 'G', 'A#'},
    'Emaj' : {'E', 'G#', 'B'},
    'Fmaj' : {'F', 'A', 'C'},
    'Gmaj' : {'G', 'B', 'D'},
    'G#maj': {'G#', 'C', 'D#'}, 
    'Amaj' : {'A', 'C#', 'E'},
    'A#maj': {'A#', 'D', 'F'},
    'Bmaj' : {'N', 'D', 'F#'},

    'Cmin' : {'C', 'D#', 'G'},
    'C#min': {'C#', 'E', 'G#'},
    'Dmin' : {'D', 'F', 'A'},
    'D#min': {'D#', 'F#', 'A#'},
    'Emin' : {'E', 'G', 'B'},
    'Fmin' : {'F', 'G#', 'C'},
    'F#min': {'F#', 'A', 'C#'}, 
    'Gmin' : {'G', 'A#', 'D'},
    'G#min': {'G#', 'B', 'D#'},
    'Amin' : {'A', 'C', 'E'},
    'A#min': {'A#', 'C#', 'F'},
    'Bmin' : {'B', 'D', 'F#'}
}


def get_chord_from_sv(state_vector) -> str:
    '''
    Returns the correct chord from the CHORD_MAP corresponding to the superposition of the 
    '''
    state_to_probability_map = [(bin(i)[2:].rjust(QUBITS, '0'), state_vector[i].real ** 2) for i in range(len(state_vector))]
    state_to_probability_map.sort(key=lambda pair: pair[1], reverse=True)
    notes = set()

    for i in range(3):
        qubit_state, probability = state_to_probability_map[i]
        notes.add(NOTE_MAP[qubit_state])

    if notes in CHORD_MAP.values():
        for chord in CHORD_MAP.keys():
            if notes == CHORD_MAP[chord]:
                return chord
    return 'INVALID_CHORD'


def get_circuit():
    try:
        qasm_str = b64decode(input("\nThe device demands an OpenQASM string encoded in base 64 from you: ")).decode()
    except:
        print("The device makes some angry noises. Perhaps there was an error decoding b64!")
        exit(0)
    try:
        circ = QuantumCircuit.from_qasm_str(qasm_str)
        circ.remove_final_measurements(inplace=True)
    except:
        print("The device looks sick from your Circuit. It advises you to use the Qiskit Transpiler in order to decompose your circuit into the basis gates (Rx. Ry, Rz, CNOT)")
        exit(0)
    if circ.num_qubits != QUBITS:
        print(f"Your quantum circuit acts on {circ.num_qubits} instead of {QUBITS} qubits!")
        exit(0)
    return circ


def main():
    print(LORE)  
    for chord in CHORD_PROGRESSION:
        circ = get_circuit()
        sv = qi.Statevector.from_instruction(circ)

        # Note from an anonymous NSA cryptanalyst: 
        # I wish there was some way I could convert a zero state vector to any arbitrary state vector of my choosing,,, I feel like I'm so close.
        input_chord = get_chord_from_sv(sv)
        if input_chord != chord:
            print("You entered the wrong chord")
            print(f"the chord you entered: {input_chord}")
            print('Good bye!')
            exit(0)
        print("Gears start shifting...")
        print("I think you entered the correct chord!")

    print("Woah... The device is shaking..,")
    print("The device has been unlocked.")
    print("you see a piece of paper hidden away inside, securely between the gears.")
    print("You pick it up and begin to read it:")
    print(FLAG)

if __name__ == "__main__":
    main()


