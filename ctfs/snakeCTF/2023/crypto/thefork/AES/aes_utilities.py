from AES.utilities import *

def forward_round(state):
    current_state = state
    current_state = sub_bytes(current_state)
    current_state = shift_rows(current_state)
    current_state = mix_columns(current_state)

    return current_state

def inverse_round(state):
    current_state = state
    current_state = inverse_mix_columns(current_state)
    current_state = inverse_shift_row(current_state)
    current_state = inverse_sub_bytes(current_state)

    return current_state