from quantum import *
from const import *

class QKD(object):


    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    

    def run(self):
        status = FAILED
        while status != SUCCESS:
            self.p1.init()
            self.p2.init()
            self.quantum_protocol()
            status = self.classical_protocol()           


    def quantum_protocol(self):
        ans = input(f"[{SEEDLEN} qubits are transmitted.]\n")
        observed = ""
        for i in range(SEEDLEN):
            qubit = self.p1.send_qubit(i)
            if 0 <= i < len(ans) and ans[i] == "1":
                collapsed_qubit, measured_bit = MAGIC_BASIS.measure(qubit)
                qubit = collapsed_qubit
                observed = observed + str(measured_bit)
            else:
                observed = observed + "?"
            self.p2.recv_qubit(qubit, i)
        print(observed)
        return SUCCESS


    def classical_protocol(self):
        basis1 = self.p1.send_basis()
        basis2 = self.p2.send_basis()
        self.p1.recv_basis(basis2)
        self.p2.recv_basis(basis1)
        index_key = [i for i in range(SEEDLEN) if basis1[i] == basis2[i]]
        index_key.sort()

        index_key_str = ','.join([str(i) for i in index_key]) + "\n"
        print(index_key_str)

        key1 = self.p1.send_key()
        key2 = self.p2.send_key()
        ber = len([i for i in range(len(key1)) if key1[i] != key2[i]]) / len(index_key)
        
        if self.p1.is_safe(ber):    
            ciphertext, nonce = self.p1.send_secret_message()
            print(ciphertext.hex())
            print(nonce.hex())
            return SUCCESS
        else:
            return FAILED