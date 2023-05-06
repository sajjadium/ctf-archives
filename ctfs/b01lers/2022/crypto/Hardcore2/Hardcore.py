import numpy as np
from os import urandom
import binascii
import hashlib
from secret import FLAG1, FLAG2

# Helpers

def digest_to_array(digest):
    hex_digest = binascii.hexlify(digest)
    binary = bin(int(hex_digest, base=16)).lstrip('0b')
    binary = np.array(list(binary))
    
    # currently leading 0s are gone, add them back
    missing_zeros = np.zeros(256 - len(binary))
    binary = np.concatenate((missing_zeros, binary.astype(int)))
    
    return binary.astype(int)

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

####################################################################################

def generate_hardcore(secret, r):
    return int(np.sum(secret * r) % 2)

def predictor(r, probability = 1):
    x_r = (r.copy() != digest_to_array(FLAG))
    np.random.seed(x_r)
    chance = np.random.rand()
    
    prediction = 0
    if chance <= probability:
        prediction = generate_hardcore(digest_to_array(FLAG), r)
    else:
        prediction = 1 - generate_hardcore(digest_to_array(FLAG), r)
        
    return int(prediction)

def parse_input():
    bitstring = input()
    assert len(bitstring) == 256
    assert set(bitstring) <= set(["0", "1"])
    
    bitstring = bitstring_to_bytes(bitstring)
    array = digest_to_array(bitstring) % 2
    return array

def Level(probability):
    hasher = hashlib.sha256()
    hasher.update(FLAG)
    encrypted_secret = hasher.hexdigest()
    problem_statement = \
        f"We're looking to find the secret behind this SHA1 hash <{str(encrypted_secret)}>. " \
         "Luckily for you, this socket takes a bitstring and predicts the dot product " \
        f"of the secret with that bit string (mod 2) with {int(100*probability)}% accuracy and sends you back the answer.\n"
        
    print(problem_statement)
    while True:
        array = parse_input()
        if array is None:
            return
        print(predictor(array, probability = probability))
    
def main():
    global FLAG
    diff = int(input("Select a difficulty (1/2):"))
    if diff == 1:
        FLAG = FLAG1
        Level(1)
    if diff == 2:
        FLAG = FLAG2
        Level(0.9)

if __name__ == "__main__":
    main()
        
