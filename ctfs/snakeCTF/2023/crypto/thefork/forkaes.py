from config import *
from AES.aes_utilities import *
from AES.utilities import *


# returns ciphertext_0 and ciphertext_1
def encrypt(plaintext, key, tweak):
    keys = key_expansion(key, TOTAL_ROUNDS+1)

    current_state = plaintext
    for i in range(HEADER_ROUNDS):
        t = add(current_state, keys[i])
        t = add(t, tweak)
        current_state = forward_round(t)

    # FORK
    current_state_path_0 = current_state
    current_state_path_1 = current_state

    # PATH 0
    for i in range(HEADER_ROUNDS, HEADER_ROUNDS+LEFT_ROUNDS):
        t = add(current_state_path_0, keys[i])
        t = add(t, tweak)
        current_state_path_0 = forward_round(t)
    
    current_state_path_0 = add(current_state_path_0, keys[HEADER_ROUNDS+LEFT_ROUNDS])
    current_state_path_0 = add(current_state_path_0, tweak)

    # PATH 1
    for i in range(HEADER_ROUNDS+LEFT_ROUNDS, TOTAL_ROUNDS):
        t = add(current_state_path_1, keys[i])
        t = add(t, tweak)
        current_state_path_1 = forward_round(t)
    current_state_path_1 = add(current_state_path_1, keys[TOTAL_ROUNDS])
    current_state_path_1 = add(current_state_path_1, tweak)

    return (current_state_path_0, current_state_path_1)



def decrypt(ciphertext, key, tweak, side="left"):
    keys = key_expansion(key, TOTAL_ROUNDS+1)
    current_state = ciphertext

    if side == "left":
        for i in range(HEADER_ROUNDS+LEFT_ROUNDS, HEADER_ROUNDS, -1):
            t = add(current_state, keys[i])
            t = add(t, tweak)
            current_state = inverse_round(t)

        current_state = add(current_state, keys[HEADER_ROUNDS])
        current_state = add(current_state, tweak)

    elif side == "right":
        for i in range(TOTAL_ROUNDS, HEADER_ROUNDS+LEFT_ROUNDS, -1):
            t = add(current_state, keys[i])
            t = add(t, tweak)
            current_state = inverse_round(t)

        current_state = add(current_state, keys[HEADER_ROUNDS+LEFT_ROUNDS])
        current_state = add(current_state, tweak)

    
    for i in range(HEADER_ROUNDS-1, -1, -1):
        t = inverse_round(current_state)
        t = add(t, tweak)
        current_state = add(t, keys[i])

    return current_state

def compute_sibling(ciphertext, key, tweak, side="left"):
    keys = key_expansion(key, TOTAL_ROUNDS+1)
    current_state = ciphertext

    if side == "left":
        for i in range(HEADER_ROUNDS+LEFT_ROUNDS, HEADER_ROUNDS, -1):
            t = add(current_state, keys[i])
            t = add(t, tweak)
            current_state = inverse_round(t)

        current_state = add(current_state, keys[HEADER_ROUNDS])
        current_state = add(current_state, tweak)

        for i in range(HEADER_ROUNDS+LEFT_ROUNDS, TOTAL_ROUNDS):
            t = add(current_state, keys[i])
            t = add(t, tweak)
            current_state = forward_round(t)
        current_state = add(current_state, keys[TOTAL_ROUNDS])
        current_state = add(current_state, tweak)

        
    elif side == "right":
        for i in range(TOTAL_ROUNDS, HEADER_ROUNDS+LEFT_ROUNDS, -1):
            t = add(current_state, keys[i])
            t = add(t, tweak)
            current_state = inverse_round(t)

        current_state = add(current_state, keys[HEADER_ROUNDS+LEFT_ROUNDS])
        current_state = add(current_state, tweak)

        for i in range(HEADER_ROUNDS, HEADER_ROUNDS+LEFT_ROUNDS):
            t = add(current_state, keys[i])
            t = add(t, tweak)
            current_state = forward_round(t)
        
        current_state = add(current_state, keys[HEADER_ROUNDS+LEFT_ROUNDS])
        current_state = add(current_state, tweak)

    return current_state