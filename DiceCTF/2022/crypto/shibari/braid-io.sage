import numpy as np
from copy import copy
    
def write_braid(braid, filename="raw_braid.txt"):
    B = braid.parent()
    gens = B.gens()
    gens_dict = {str(b):i for i,b in enumerate(list(gens))}

    res = []
    for b,e in braid.syllables():
        x = gens_dict[str(b)] + 1
        if e < 0:
            x = -x
        for j in range(abs(e)):
            res.append(x)

    with open(filename, "w") as f:
        r = [str(i) for i in res]
        s = " ".join(r)
        f.write(s)


class BraidCircuitEvaluator:
    def __init__(self):
        G = AlternatingGroup(5)

        G_elements = list(G)
        G_elements_map_fwd = {i:j for j,i in enumerate(G_elements)}
        G_elements_map_bck = {i:j for i,j in enumerate(G_elements)}

        N = len(G_elements)
        multiplication_table = np.zeros((N,N), dtype=int)
        for i in range(N):
            for j in range(N):
                tmp = G_elements_map_bck[i] * G_elements_map_bck[j]
                res = G_elements_map_fwd[tmp]
                multiplication_table[i][j] = res

        R_conjugation_table = np.zeros((N,N), dtype=int)
        for i in range(N):
            for j in range(N):
                tmp = G_elements_map_bck[j]^(-1) * G_elements_map_bck[i] * G_elements_map_bck[j]
                res = G_elements_map_fwd[tmp]
                R_conjugation_table[i][j] = res

        Rinv_conjugation_table = np.zeros((N,N), dtype=int)
        for i in range(N):
            for j in range(N):
                tmp = G_elements_map_bck[i] * G_elements_map_bck[j] * G_elements_map_bck[i]^(-1)
                res = G_elements_map_fwd[tmp]
                Rinv_conjugation_table[i][j] = res

        inverse_table = np.zeros(N, dtype=int)
        for i in range(N):
            tmp = G_elements_map_bck[i]^(-1)
            res = G_elements_map_fwd[tmp]
            inverse_table[i] = res
        
        self.N = N
        self.G = G
        self.multiplication_table = multiplication_table
        self.inverse_table = inverse_table
        self.R_conjugation_table = R_conjugation_table
        self.Rinv_conjugation_table = Rinv_conjugation_table
        self.G_elements_map_fwd = G_elements_map_fwd
        self.G_elements_map_bck = G_elements_map_bck
    
    def encode_bits(self, bits):
        G = self.G
        ancilla_521   = G([5,1,3,4,2])
        ancilla_14352 = G([4,1,5,3,2])
        ancilla_124   = G([2,4,3,1,5])
        ancilla_15342 = G([5,1,4,2,3])
        
        encoded_one  = G([1,2,5,3,4])
        encoded_zero = G([1,2,4,5,3])

        ancilla_registers = []
        for i in [ancilla_14352, ancilla_15342, ancilla_124, ancilla_521]:
            x = self.G_elements_map_fwd[i]
            x_inv = self.inverse_table[x]
            ancilla_registers.append(x)
            ancilla_registers.append(x_inv)

        encoded_one_registers = []
        i = encoded_one
        x = self.G_elements_map_fwd[i]
        x_inv = self.inverse_table[x]
        encoded_one_registers.append(x)
        encoded_one_registers.append(x_inv)

        encoded_zero_registers = []
        i = encoded_zero
        x = self.G_elements_map_fwd[i]
        x_inv = self.inverse_table[x]
        encoded_zero_registers.append(x)
        encoded_zero_registers.append(x_inv)
        
        registers = copy(ancilla_registers)
        for b in bits:
            if b == 0:
                registers += encoded_zero_registers
            else:
                registers += encoded_one_registers
                
        return registers

    def apply_R_gate(self, registers, n):
        registers = copy(registers)
        r1 = registers[n]
        r2 = registers[n+1]

        tmp = self.R_conjugation_table[r1][r2]
        registers[n] = r2
        registers[n+1] = tmp
        return registers

    def apply_R_inv_gate(self, registers, n):
        registers = copy(registers)
        r1 = registers[n]
        r2 = registers[n+1]

        tmp = self.Rinv_conjugation_table[r1][r2]
        registers[n+1] = r1
        registers[n] = tmp
        return registers
    
    def apply_braid(self, registers, braid):
        B = braid.parent()
        gens = B.gens()
        gens_dict = {str(b):i for i,b in enumerate(gens)}
        
        if len(registers) != len(B.gens()) + 1:
            raise ValueError(f"mismatch between number of "\
                             "registers = {len(registers)} and BraidGroup = {B}")
        
        registers = copy(registers)
        for b,e in braid.syllables():
            i = gens_dict[str(b)]
            f = [self.apply_R_gate, self.apply_R_inv_gate][e<0]
            for j in range(abs(e)):
                registers = f(registers, i)
            
        return registers
    
    def decode_registers(self, registers):
        registers = registers[8::2]
        registers = [1 if i == 20 else 0 if i == 40 else None for i in registers]
        return registers
        
class BraidCircuitCompiler:
    def __init__(self, n):
        B = BraidGroup(2*(n+4))
        gens = list(B.gens())
        
        self.n = n
        self.B = B
        self.gens = gens
                
        self.idx_521   = 0
        self.idx_14352 = 1
        self.idx_124   = 2
        self.idx_15342 = 3
    
    def get_identity_gate(self):
        g = self.gens[0]
        return g * ~g
    
    def get_R_gate(self, idx):
        return self.gens[idx]
    
    def get_Rinv_gate(self, idx):
        return ~self.gens[idx]
    
    def get_C_gate_immediate(self, m):
        n = 2 * m + 1
        return prod([self.gens[i] for i in [n,n+1,n+1,n]])
    
    def get_Cinv_gate_immediate(self, m):
        n = 2 * m + 1
        return prod([~self.gens[i] for i in [n,n+1,n+1,n]])
    
    def get_swap_gate(self, m):
        n = 2 * m + 1
        return prod([self.gens[i] for i in [n,n-1,n+1,n]])
    
    def prod(self, X):
        p = prod(X)
        if p == 1:
            return self.get_identity_gate()
        return p
    
    def get_C_gate(self, m0, m1):
        if m0 < m1:
            I = list(range(m0, m1 - 1))
            p = self.prod([self.get_swap_gate(i) for i in I])
            C = self.get_C_gate_immediate(m1 - 1)
            
            return p * C * ~p

        I = list(range(m1, m0))    
        p = self.prod([self.get_swap_gate(i) for i in I])
        C = self.get_C_gate_immediate(m1)
        
        return ~p * C * p
    
    def get_Cinv_gate(self, m0, m1):
        if m0 < m1:
            I = list(range(m0, m1 - 1))
            p = self.prod([self.get_swap_gate(i) for i in I])
            C = self.get_Cinv_gate_immediate(m1 - 1)
            
            return p * C * ~p

        I = list(range(m1, m0))    
        p = self.prod([self.get_swap_gate(i) for i in I])
        C = self.get_Cinv_gate_immediate(m1)

        return ~p * C * p
    
    """
    g1, g2 = controls
    g0 = target
    """
    def get_CCX_gate(self, g1, g2, g0):
        for g in [g0,g1,g2]:
            if g < 0:
                raise ValueError("cannot use ancilla registers as input")
                
        g0 = g0 + 4
        g1 = g1 + 4
        g2 = g2 + 4
        
        res = prod([
            self.get_C_gate(self.idx_15342, g0),
            self.get_C_gate(g1, g0),
            self.get_C_gate(self.idx_521, g0),
            self.get_C_gate(g2, g0),
            self.get_C_gate(self.idx_124, g0),
            self.get_Cinv_gate(g1, g0),
            self.get_C_gate(self.idx_14352, g0),
            self.get_Cinv_gate(g2, g0),
            self.get_C_gate(self.idx_14352, g0)
        ])
        return res
    
    """
    g1 = control
    g0 = target
    """
    def get_CX_gate(self, g1, g0):
        return self.get_CCX_gate(g1, g1, g0)
    
    def get_X_gate(self, m):
        n = 2 * (m+4)
        return self.gens[n]
    
