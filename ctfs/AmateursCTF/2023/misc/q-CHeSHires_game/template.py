from base64 import b64encode
from qiskit import QuantumCircuit

# alice_x_0
alice_x_0 = QuantumCircuit(2, 1)
## define your circuit here

# alice_x_1
alice_x_1 = QuantumCircuit(2, 1)
## define your circuit here

# bob_y_0
bob_y_0 = QuantumCircuit(2, 1)
## define your circuit here

# bob_y_1
bob_y_1 = QuantumCircuit(2, 1)
## define your circuit here



strategies = [alice_x_0, alice_x_1, bob_y_0, bob_y_1]
strategies = [b64encode(qc.qasm().encode()) for qc in strategies]

# send strategies to server
from pwn import remote
r = remote('amt.rs', 31011)

for strategy in strategies:
    r.sendline(strategy)

print(r.recvall())
