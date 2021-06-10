import numpy as np
import random
from os import urandom
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import AES

from qiskit import (
    QuantumCircuit, 
    QuantumRegister, 
    ClassicalRegister,
    Aer, 
    assemble
)
from qiskit.quantum_info.operators import Operator

class Bank:
    def __init__(self):
        # Avoid other clients from messing with us
        self.r = random.Random()
        self.num_bits = 30
        self.key = urandom(16)
        # For each medallion bit, we give 3 qubits for users
        # to play around with. q0 is the one that belongs to the
        # medallion, and q1, q2 are for user experiments (ancilla
        # if you will). We initialize to |000> here.
        self.state_vecs = [np.array([1,0,0,0,0,0,0,0]) 
            for _ in range(self.num_bits)]
    
    def aes_enc(self, m):
        return AES.new(self.key, AES.MODE_ECB).encrypt(m)

    def aes_dec(self, c):
        return AES.new(self.key, AES.MODE_ECB).decrypt(c)

    def refresh_bank(self):
        self.key = urandom(16)

    # Return the medallion id of a new medallion
    def new_medallion(self):
        bases = self.r.getrandbits(self.num_bits)
        bits = self.r.getrandbits(self.num_bits)
        res = ((bits << self.num_bits) + bases).to_bytes(16, 'big')
        for i in range(self.num_bits):
            qr = QuantumRegister(3)
            cr = ClassicalRegister(1)
            qc = QuantumCircuit(qr, cr)
            qc.initialize(self.state_vecs[i], qr)
            qc.measure(0, 0)
            qc.initialize(np.array([1,0]), [qr[0]])
            if bases % 2:
                if bits % 2:
                    # This gives |->
                    qc.x(0)
                    qc.h(0)
                else:
                    # This gives |+>
                    qc.h(0)
            else:
                if bits % 2:
                    # This gives |1>
                    qc.x(0)
                else:
                    # This gives |0>, cuz why not
                    qc.x(0)
                    qc.x(0)
            sv_sim = Aer.get_backend('statevector_simulator')
            qobj = assemble(qc)
            job = sv_sim.run(qobj)
            self.state_vecs[i] = job.result().get_statevector()
            bases //= 2
            bits //= 2
        return bytes_to_long(self.aes_dec(res))
    
    # Given medallion id, measure in the corresponding bases and check
    # correctness.
    def verify_medallion(self, medallion_id):
        desired = bytes_to_long(self.aes_enc(medallion_id.to_bytes(16, 'big')))
        if desired >= (1 << (2 * self.num_bits)):
            return False
        for i in range(self.num_bits):
            qr = QuantumRegister(3)
            cr = ClassicalRegister(1)
            qc = QuantumCircuit(qr, cr)
            sv_sim = Aer.get_backend('statevector_simulator')
            qc.initialize(self.state_vecs[i], qr)
            if desired & (1 << i):
                qc.h(0)
            qc.measure(0, 0)
            qobj = assemble(qc)
            job = sv_sim.run(qobj)
            measure_res = job.result().get_counts()
            self.state_vecs[i] = job.result().get_statevector()
            if desired & (1 << (i + self.num_bits)):
                if ('1' not in measure_res) or ('0' in measure_res):
                    return False
            else:
                if ('0' not in measure_res) or ('1' in measure_res):
                    return False
            # Reinitialize to 0
            if '1' in measure_res:
                qr = QuantumRegister(3)
                cr = ClassicalRegister(1)
                qc = QuantumCircuit(qr, cr)
                qc.initialize(self.state_vecs[i], qr)
                qc.x(0)
                job = sv_sim.run(assemble(qc))
                self.state_vecs[i] = job.result().get_statevector()
        return True

    # Get the string representation of the medallion
    def get_medallion(self, medallion_id):
        desired = bytes_to_long(self.aes_enc(medallion_id.to_bytes(16, 'big')))
        res = ''
        for i in range(self.num_bits):
            if desired & (1 << i):
                if desired & (1 << (i + self.num_bits)):
                    res += '-'
                else:
                    res += '+'
            else:
                if desired & (1 << (i + self.num_bits)):
                    res += '1'
                else:
                    res += '0'
        return res
    
    '''
    Allowed operations on medallions:
    1. X gate
    2. Y gate
    3. Z gate
    4. Hadamard gate
    5. Identity gate
    6. Rx gate
    7. Ry gate
    8. Rz gate
    9. CNOT gate
    10. SWAP gate
    11. CCNOT gate
    12. Unitary transform
    13. Measure in 0/1 basis
    Given {"operation": 1, "qubit": 5, "params": [0]}, we apply NOT gate on the
    0th qubit for the 5th medallion bit. We return error if anything goes
    wrong.
    '''
    def operate_on_medallion(self, data):
        if (('operation' not in data) or ('params' not in data) or 
            ('qubit' not in data)):
            return {'error': 'data invalid'}
        try:
            qubit = data['qubit']
            state_vec = self.state_vecs[qubit]
            qc = QuantumCircuit()
            qr = QuantumRegister(3)
            cr = ClassicalRegister(1)
            qc.add_register(qr, cr)
            qc.initialize(state_vec, qr)
            if data['operation'] == 1:
                qc.x(*data['params'])
            elif data['operation'] == 2:
                qc.y(*data['params'])
            elif data['operation'] == 3:
                qc.z(*data['params'])
            elif data['operation'] == 4:
                qc.h(*data['params'])
            elif data['operation'] == 5:
                qc.i(*data['params'])
            elif data['operation'] == 6:
                qc.rx(*data['params'])
            elif data['operation'] == 7:
                qc.ry(*data['params'])
            elif data['operation'] == 8:
                qc.rz(*data['params'])
            elif data['operation'] == 9:
                qc.cx(*data['params'])
            elif data['operation'] == 10:
                qc.swap(*data['params'])
            elif data['operation'] == 11:
                qc.ccx(*data['params'])
            elif data['operation'] == 12:
                op = Operator(np.array(data['params']).reshape(8,8))
                qc.unitary(op, [qr[0], qr[1], qr[2]])
            elif data['operation'] == 13:
                qc.measure(data['params'][0], 0)
            else:
                raise ValueError('operation not recognized')
            sv_sim = Aer.get_backend('statevector_simulator')
            qobj = assemble(qc)
            job = sv_sim.run(qobj)
            self.state_vecs[qubit] = job.result().get_statevector()
            if data['operation'] != 13:
                return {'msg': 'operation complete'}
            else:
                measure_res = job.result().get_counts()
                if '0' in measure_res:
                    return {'msg': 'measurement gives 0'}
                elif '1' in measure_res:
                    return {'msg': 'measurement gives 1'}
                else:
                    raise ValueError('bad measurement result')
        except Exception as e:
            return {'error': str(e)}
