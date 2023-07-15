from qiskit import QuantumCircuit
from qiskit import Aer, execute

backend = Aer.get_backend('qasm_simulator')
def encode(bits):
    circuit = QuantumCircuit(8)
    for i, bit in enumerate(bits):
        if bit == '1':
            circuit.x(i)
        
    for i in range(7, 0, -1):
        circuit.cx(i, i-1)
    
    circuit.measure_all()
    job = execute(circuit, backend, shots=1)
    result = job.result()
    result = list(result.get_counts().keys())[0][::-1]

    ret = int(bits, 2) ^ int(result, 2)
    return ret

flag = b"amateursCTF{REDACTED}"
enc = b""
for i in flag:
    enc += bytes([encode(bin(i)[2:].zfill(8))])

print(enc, enc.hex())
# b'\xbe\xb6\xbeXF\xa6\\\xa2\x82\x98\x84R\xb4 X\xb0N\xb4\xbaj^f\xd8\xb4X\xa6\xb6j\xd8\xbc \xa6XjX\xb0\xde\xa2j\xd8Xj~HHV'  beb6be5846a65ca282988452b42058b04eb4ba6a5e66d8b458a6b66ad8bc20a6586a58b0dea26ad8586a7e484856