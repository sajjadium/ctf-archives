import numpy as np


class Qubit(object):
    "A (pure) qubit."

    def __init__(self, v:list):
        assert len(v) == 2
        norm = (abs(v[0])**2 + abs(v[1])**2)**0.5
        self.v = np.array(v) / norm


    def orthogonal(self):
        return Qubit(np.conj([self.v[1], -self.v[0]]))


class Basis(object):
    "A basis for C^2."

    def __init__(self, qubit:Qubit):
        self.basis = [qubit, qubit.orthogonal()]


    def measure(self, q:Qubit, verbose=False):
        "Measure a qubit."

        probability = [abs(np.vdot(q.v, self.basis[0].v))**2,
                   abs(np.vdot(q.v, self.basis[1].v))**2]
        probability = probability / sum(probability)
    
        if verbose:
            print(probability)
        measured_bit = np.random.choice(2, p=probability)
        collapased_qubit = self.basis[measured_bit]

        return collapased_qubit, measured_bit


PAULI_BASES = [Basis(Qubit([1+0j, 1+0j])), Basis(Qubit([1+0j, 0+0j]))]
THETA = np.pi/8
MAGIC_QUBIT = Qubit([np.cos(THETA)+0j, np.sin(THETA)+0j])
MAGIC_BASIS = Basis(MAGIC_QUBIT)