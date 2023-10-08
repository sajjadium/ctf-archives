import os
import random
import bitstring
from Crypto.Cipher import AES
from quantum import *
from const import *


class Player(object):
    

    def __init__(self, msg=""):
        self.seed = bitstring.BitArray(os.urandom(SEEDLEN//8))
        self.key = None
        self.basis = None
        self.msg = msg


    def init(self):
        self.basis = bitstring.BitArray(os.urandom(SEEDLEN//8))


    def send_qubit(self, index):
        return PAULI_BASES[self.basis[index]].basis[self.seed[index]]


    def recv_qubit(self, qubit, index):
        _, measured_bit = PAULI_BASES[self.basis[index]].measure(qubit)
        self.seed[index] = measured_bit


    def send_basis(self):
        return self.basis


    def recv_basis(self, basis):
        index_same_basis = [i for i in range(SEEDLEN) if self.basis[i] == basis[i]]
        self.key = self.seed[index_same_basis]


    def send_key(self):
        return self.key


    def is_safe(self, ber):
        return (len(self.key) >= KEYLEN) and (ber > THRESHOLD)


    def send_secret_message(self):
        key_in_bytes = self.key[0:KEYLEN].tobytes()
        cipher = AES.new(key_in_bytes, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(self.msg.encode())
        return ciphertext, nonce