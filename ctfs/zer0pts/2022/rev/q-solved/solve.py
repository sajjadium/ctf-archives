import gmpy2
from qiskit import QuantumCircuit, execute, Aer
from qiskit.circuit.library import XGate
import json

with open("circuit.json", "r") as f:
    circ = json.load(f)

nq = circ['memory']
na = circ['ancilla']
target = nq + na

print("[+] Constructing circuit...")
main = QuantumCircuit(nq + na + 1, nq)
sub = QuantumCircuit(nq + na + 1)

main.x(target)
main.h(target)
for i in range(circ['memory']):
    main.h(i)

t = circ['memory']
for cs in circ['circuit']:
    ctrl = ''.join(['0' if x else '1' for (x, _) in cs])
    l = [c for (_, c) in cs]
    sub.append(XGate().control(len(cs), ctrl_state=ctrl), l + [t])
    t += 1

sub.append(XGate().control(na, ctrl_state='0'*na),
           [i for i in range(nq, nq + na)] + [target])

for cs in circ['circuit'][::-1]:
    t -= 1
    ctrl = ''.join(['0' if x else '1' for (x, _) in cs])
    l = [c for (_, c) in cs]
    sub.append(XGate().control(len(cs), ctrl_state=ctrl), l + [t])

sub.h([i for i in range(nq)])
sub.append(XGate().control(nq, ctrl_state='0'*nq),
           [i for i in range(nq)] + [target])
sub.h([i for i in range(nq)])

for i in range(round(0.785 * int(gmpy2.isqrt(2**nq)) - 0.5)):
    main.append(sub, [i for i in range(na + nq + 1)])

for i in range(nq):
    main.measure(i, i)

print("[+] Calculating flag...")
emulator = Aer.get_backend('qasm_simulator')
job = execute(main, emulator, shots=1024)
hist = job.result().get_counts()
result = sorted(hist.items(), key=lambda x: -x[1])[0][0]

print("[+] FLAG:")
print(int.to_bytes(int(result, 2), nq//8, 'little'))
