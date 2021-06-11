import base64
import random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from qulacs import QuantumState, QuantumCircuit
from qulacs.gate import *
from secret import flag

GATES = {
    'CNOT': (CNOT, 2),
    'H': (H, 1), 'X': (X, 1), 'Y': (Y, 1), 'Z': (Z, 1),
    'S': (S, 1), 'SDAG': (Sdag, 1), 'T': (T, 1), 'TDAG': (Tdag, 1)
}
def parse_circuit(asm, qbits=9):
    """ Convert assembly into quantum circuit
    i.e.  q0 ---+--[Z]--
                |        <= CNOT 0,1; Z 0; H 1;
          q1 --[X]-[H]--
    """
    def apply(gate, args):
        return gate(*args)

    circuit = QuantumCircuit(qbits)
    cnt = 0
    for instruction in asm.replace('\n', '').split(';'):
        t = instruction.strip().split()
        if t == []:
            continue

        if len(t) < 2:
            print("[-] Invalid instruction")
            exit(0)

        opecode, operand = t[0].upper(), t[1:]
        if opecode not in GATES:
            print("[-] Invalid gate")
            exit(0)

        operand = list(map(lambda x: int(x), ''.join(t[1:]).split(',')))
        if not all(map(lambda x: 0 <= x < qbits, operand)):
            print("[-] Invalid quantum bit specified")
            exit(0)

        if GATES[opecode][1] != len(operand):
            print("[-] Invalid number of operands")
            exit(0)

        gate = apply(GATES[opecode][0], operand)
        circuit.add_gate(gate)

        cnt += 1
        if cnt > 100:
            print("[-] Too large circuit")
            exit(0)

    return circuit

def transfer_and_measure(q):
    # Oops, noise might happen :(
    noise = QuantumCircuit(9)
    idx = random.randrange(0, 9)
    noise.add_gate(DephasingNoise(idx, 0.31337))
    noise.add_gate(DepolarizingNoise(idx, 0.31337))
    noise.add_gate(BitFlipNoise(idx, 0.31337))
    noise.update_quantum_state(q)

    # Quantum arrived! You can update (or keep) the state :)
    circuit = parse_circuit(input('[?] Your Circuit: '))
    circuit.update_quantum_state(q)

    # Now you measure the quantum state :P
    return random.choices(range(2**9),
                          map(lambda x: abs(x), q.get_vector()))[0] & 1

if __name__ == '__main__':
    N = 128
    xi, xip = 0.98, 0.98
    p = (xi * (1 + xi))**0.5 - xi
    Np = int(N * (1 + 2*xi + 2*(xi*(1+xi))**0.5 + xip))
    print("[+] Np = " + str(Np))

    encoder = parse_circuit("""
    CNOT 0,3; CNOT 0,6;
    H 0; H 3; H 6;
    CNOT 0,1; CNOT 0,2;
    CNOT 3,4; CNOT 3,5;
    CNOT 6,7; CNOT 6,8;
    """)

    measured = 0
    ra, ba = 0, 0
    for i in range(Np):
        ra = (ra << 1) | random.choice([0, 1])
        ba = (ba << 1) | random.choices([1, 0], [p, 1-p])[0]
        q = QuantumState(9)
        q.set_zero_state()
        if ra & 1:
            X(0).update_quantum_state(q)
        if ba & 1:
            H(0).update_quantum_state(q)
        encoder.update_quantum_state(q)

        measured = (measured << 1) | transfer_and_measure(q)
        del q

    print("[+] Measured state: " + bin(measured))
    bb = int(input('[?] bb = '), 2)
    print("[+] ba = " + bin(ba))

    Nx, Nz = 0, 0
    for i in range(Np):
        if (ba >> i) & 1 == (bb >> i) & 1 == 1:
            Nx += 1
        elif (ba >> i) & 1 == (bb >> i) & 1 == 0:
            Nz += 1
    if Nx < N * xi or Nz - N < N * xi:
        print("[-] Something went wrong :(")
        exit(0)

    xa = 0
    for i in range(Np):
        if (ba >> i) & 1 == (bb >> i) & 1 == 1:
            xa = (xa << 1) | ((ra >> i) & 1)
    print("[+] xa = " + bin(xa))

    l = []
    for i in range(Np):
        if (ba >> i) & 1 == (bb >> i) & 1 == 0:
            l.append(i)
    chosen = random.sample(l, Nz - N)
    m = 0
    for i in chosen:
        m |= 1 << i
    print("[+] m = " + bin(m))

    k = 0
    for i in sorted(list(set(l) - set(chosen))):
        k = (k << 1) | ((ra >> i) & 1)

    key = int.to_bytes(k, N // 8, 'big')
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ct = cipher.encrypt(pad(flag, AES.block_size))
    print("Result: " + base64.b64encode(iv + ct).decode())
