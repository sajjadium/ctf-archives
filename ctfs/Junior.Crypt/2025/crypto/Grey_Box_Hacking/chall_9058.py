def lfsr(state, mask):
    # Generating a new bit and updating the state LFSR
    feedback = (state & 1)  # Least bit (standard for right-shift LFSR)
    state = state >> 1      # Right shift
    if feedback:
        state ^= mask       # Using a feedback mask
    return state, feedback

initial_state = 0x????  # 16-bit initial state
mask          = 0x????  # 16-bit feedback mask

b64_Enc_XOR_text = "rKcUtOpHHO6ZXNzB3IwyLXPzQX9pkAYLNfrolB191POUEJoz3xQANLSTm1inSV3jh88w15d5jcaQttzpNyewT7mPufbvtVf+xMTS7Zeeai4u6/TyeFHGLPH9cHnCNg=="

"""
def lfsr(state, mask):
        # state: the current state of the LFSR, represented as an integer.
        #        For example, for a 4-bit LFSR, if the state is [1,0,0,0], then state = 8 (or 0b1000).
        # mask: a feedback mask that determines which bits participate in the XOR.
        #        Each set bit in the mask corresponds to a "tap" in the LFSR.
        #        For example, for a polynomial x^4 + x^3 + 1, the mask could be 0b1100 (for 4-bit)
        #        or 0b1001 (for 4-bit, if 1 is x^0 and 4 is x^3)

    feedback = (state & 1)
    
        # This is the key. In this style of implementation (a Galois LFSR with right shifting),
        # the output bit (the one used for feedback, and often the
        # output of the entire LFSR) is the **least significant bit** (LSB) of the current state.
        # The `& 1` operation effectively extracts this least significant bit.

    state = state >> 1 # Right shift
    
        # All bits in the register are shifted one place to the right. The least significant bit that we
        # just saved in `feedback` is dropped.

    if feedback:
    state ^= mask # Using a feedback mask
    
        # This is the heart of the Galois LFSR. If the `feedback` bit (i.e. the least significant bit before the shift) is 1,
        # then the **new state** is XORed with the mask. This creates the effect that the
        # "taps" (defined by the mask) are changed. If the `feedback` bit is 0,
        # then no change (XOR with 0) occurs.

    return state, feedback

        # The function returns the new state of the LFSR and the bit that was "thrown out" (output_bit / feedback_bit).
"""