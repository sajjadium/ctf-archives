import numpy as np

from .rescue_constants import MDS_MATRIX, NUM_ROUNDS, PRIME, ROUND_CONSTANTS, WORD_SIZE


def pow_mod(vector: np.ndarray, exponent: int, p: int) -> np.ndarray:
    """
    Returns a numpy array which, in index i, will be equal to (vector[i] ** exponent % p), where
    '**' is the power operator.
    """
    return np.vectorize(lambda x: pow(x, exponent, p))(vector)


def rescue_hash(
        inputs, mds_matrix=MDS_MATRIX, round_constants=ROUND_CONSTANTS,
        word_size=WORD_SIZE, p=PRIME, num_rounds=NUM_ROUNDS):
    """
    Returns the result of the Rescue hash on the given input.
    The state size is word_size * 3.
    inputs is a list/np.array of size (word_size * 2)
    round_constants consists of (2 * num_rounds + 1) vectors, each of the same size as state size.
    mds_matrix is an MDS (Maximum Distance Separable) matrix of size (state size)x(state size).
    """

    mds_matrix = np.array(mds_matrix, dtype=object) % p
    round_constants = np.array(round_constants, dtype=object)[:, :, np.newaxis] % p
    inputs = np.array(inputs, dtype=object).reshape(2 * word_size, 1) % p
    zeros = np.zeros((word_size, 1), dtype=object)
    state = np.concatenate((inputs, zeros))
    #print("state:", [x[0] for x in state])
    state = (state + round_constants[0]) % p

    for i in range(1, 2 * num_rounds, 2):
        # First half of round i/2.
        #print("before first half", [x[0] for x in state])
        state = pow_mod(state, (2 * p - 1) // 3, p)
        state = mds_matrix.dot(state) % p
        state = (state + round_constants[i]) % p
        # Second half of round i/2.
        #print("before second half", [x[0] for x in state])

        state = pow_mod(state, 3, p)
        state = mds_matrix.dot(state) % p
        state = (state + round_constants[i + 1]) % p
    return (state[:word_size].flatten() % p).tolist()

def rescue(input):
    inp = input[:8]
    ind = 8
    while ind < len(input):
        res = rescue_hash(inp)
        inp = res + input[ind: ind + 4]
        ind += 4
    return rescue_hash(inp)
