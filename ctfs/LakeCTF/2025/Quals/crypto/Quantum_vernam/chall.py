#!/usr/bin/env -S python3 -u
import os
import numpy as np
from math import sqrt
# no need quantum libraries here, only linear algebra. 
from scipy.stats import unitary_group



def string_to_bits(s): 
    bits = []
    for byte in s:
        for i in range(8):
            bits.append((byte >> (7 - i)) & 1)
    return bits

def bit_to_qubit(bit):
    if bit == 0:
        return np.array([1,0])  # |0>
    else:
        return np.array([0, 1]) # |1>

def encryption(key, message,gate1,gate2,x):
    key_bits = string_to_bits(key)
    message_bits = string_to_bits(message)
    cipher = []
    


    encryption_matrix = np.array([])
    PauliX = np.array([(0,1), (1,0)])
    PauliZ = np.array([(1,0), (0,-1)])

    for k, m in zip(key_bits, message_bits):
        qubit = bit_to_qubit(m)
        qubit = gate1 @ qubit

        if k == 1:
            qubit =  x @ qubit

        qubit = gate2 @ qubit
        cipher.append(qubit)
    return cipher

def measurement(cipher):
    measured_bits = []
    for qubit in cipher:
        prob_0 = qubit[0]*qubit[0].conjugate()

        if np.random.rand() < prob_0:
            measured_bits.append(0)
        else:
            measured_bits.append(1)
    return measured_bits

def bits_to_string(bits):
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | bits[i + j]
        bytes_list.append(byte)
    return bytes(bytes_list)
    
####################################################################################


FLAG = b"EPFL{FAKEFLAAAAAAAG}}"
n = len(FLAG)
key = os.urandom(n)
x = unitary_group.rvs(2)


print("Welcome to the Quantum Vernam Cipher Encryption! Key and flag have same length, try to break perfect secrecy if you can.")
print("\n")
print('The qubits will be encrypted with the matrix x = ',x)
print("\n")
print("You can apply any gate you want to the qubits before and after measurement as a 2X2 matrix, choose your favorite one :)")
print("\n")
print("Also pls remember that in python, j is the imaginary unit, not i.")
print('\n')
print('Enter coefficients for the first matrix that will be applied BEFORE encryption:')
print('Enter first matrix element:') 
a1 = complex(input())
print('Enter second matrix element:')
b1 = complex(input())
print('Enter third matrix element:')
c1 = complex(input())
print('Enter fourth matrix element:')
d1 = complex(input())

gate1 = np.array([(a1,b1),(c1,d1)])



print('\n')
print('Enter coefficients for the second matrix that will be applied AFTER encryption:')
print('Enter first matrix element:') 
a2 = complex(input())
print('Enter second matrix element:')
b2 = complex(input())
print('Enter third matrix element:')
c2 = complex(input())
print('Enter fourth matrix element:')
d2 = complex(input())

gate2 = np.array([(a2,b2),(c2,d2)])



# vérifie que les matrices sont unitaires
def is_unitary(matrix):
    identity = np.eye(matrix.shape[0])
    return np.allclose(matrix.conj().T @ matrix, identity)


    
assert is_unitary(gate1), "Gate 1 is not unitary!"  
assert is_unitary(gate2), "Gate 2 is not unitary!"


cipher = encryption(key, FLAG,gate1,gate2,x)
measurement_result = measurement(cipher)


print("measurement:", measurement_result)
print(bits_to_string(measurement_result))
