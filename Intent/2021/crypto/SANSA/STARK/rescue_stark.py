import numpy as np
from math import ceil, log
import time
from .rescue.rescue_constants   import MDS_MATRIX, INV_MDS_MATRIX,  ROUND_CONSTANTS, PRIME, WORD_SIZE, NUM_ROUNDS, STATE_SIZE
from .poly_utils import PrimeField
from .utils import get_power_cycle, get_pseudorandom_indices, is_a_power_of_2
from .fft import fft
from .fri import prove_low_degree, verify_low_degree_proof
from .permuted_tree import merkelize, mk_branch, verify_branch, blake, mk_multi_branch, verify_multi_branch
import random

modulus = PRIME
extension_factor = 8
f = PrimeField(modulus)
TRACE_SIZE = 16
RAND_BEFORE = 1
RAND_AFTER = 0
spot_check_security_factor = 20
BatchHeight = 32
HashesPerBatch = 3
constraints_powers_dict = {i : (lambda x,y:0) for i in range(20)}
constrains_power_dict = {
    0: lambda total_power, comp_length: total_power - comp_length,
    1: lambda total_power, comp_length: total_power - comp_length,
    2: lambda total_power, comp_length: total_power - 6*comp_length,
    3: lambda total_power, comp_length: total_power - 6*comp_length,
    4: lambda total_power, comp_length: total_power - 6*comp_length,
    5: lambda total_power, comp_length: total_power - 6*comp_length,
    6: lambda total_power, comp_length: total_power - 4*comp_length,
    7: lambda total_power, comp_length: total_power - comp_length,
    8: lambda total_power, comp_length: total_power - comp_length,
    9: lambda total_power, comp_length: total_power - comp_length,
    10: lambda total_power, comp_length: total_power - comp_length,
    11: lambda total_power, comp_length: total_power - comp_length,
    12: lambda total_power, comp_length: total_power - comp_length,
    13: lambda total_power, comp_length: total_power - comp_length,
    14: lambda total_power, comp_length: total_power - comp_length,
    15: lambda total_power, comp_length: total_power - comp_length,
    16: lambda total_power, comp_length: total_power - comp_length,
    17: lambda total_power, comp_length: total_power - comp_length,
    18: lambda total_power, comp_length: total_power - comp_length,
    19: lambda total_power, comp_length: total_power - comp_length,
}
NUM_CONSTRAINTS = 200

def HalfRound(state, round_index, p):
    mds_matrix = np.array(MDS_MATRIX, dtype=object) % p

    if round_index % 2 == 1:
        state = [pow(x, (2*p - 1) // 3, p) for x in state]
    else:
        state = [pow(x, 3, p) for x in state]
    state = mds_matrix.dot(state) % p
    state = [(state[i] + ROUND_CONSTANTS[round_index][i]) % p for i in range(STATE_SIZE)]
    return state

def get_power_list(total_length, comp_length, hash = True):
    powers = []
    for i in range(4):
        powers.append(constraints_powers_dict[0](total_length, comp_length))
    for i in range(4):
        powers.append(constraints_powers_dict[1](total_length, comp_length))
    for i in range(STATE_SIZE):
        powers.append(constraints_powers_dict[2](total_length, comp_length))
    for i in range(4):
        powers.append(constraints_powers_dict[3](total_length, comp_length))
    for i in range(STATE_SIZE - 4):
        powers.append(constraints_powers_dict[4](total_length, comp_length))
    for i in range(4):
        powers.append(constraints_powers_dict[5](total_length, comp_length))
    for i in range(STATE_SIZE):
        powers.append(constraints_powers_dict[6](total_length, comp_length))
    for i in range(4):
        powers.append(constraints_powers_dict[7](total_length, comp_length))
    for i in range(4):
        powers.append(constraints_powers_dict[8](total_length, comp_length))
    for i in range(STATE_SIZE*STATE_SIZE):
        powers.append(constraints_powers_dict[9](total_length, comp_length))
    if hash:
        for i in range(4):
            powers.append(constraints_powers_dict[10](total_length, comp_length))
    for i in range(TRACE_SIZE + 1):
        powers.append(total_length - comp_length)
    return powers


def append_state(trace, state):
    for i in range(STATE_SIZE):
        trace[i].append(state[i])
    for i in range(STATE_SIZE, TRACE_SIZE):
        trace[i].append(0)

def rescue_computational_trace(input, file_hash = None, output = None):
    input_length = len(input)
    if file_hash is not None:
        input_and_hash = input + [random.randrange(1, PRIME) for _ in range(12*RAND_BEFORE)] + file_hash + [random.randrange(1, PRIME) for _ in range(8 + 12*RAND_AFTER)]
    else:
        input_and_hash = input[:]
    inp_hash_length = len(input_and_hash)
    chain_length = ceil((inp_hash_length - 4) / 4)
    # We do HashesPerBatch so that the total append_states amount will be BatchHeight, which is a power of two
    log_trace_length = log(ceil(chain_length / HashesPerBatch), 2)
    # We want to have a power of 2 number of batches, so that the total height will also be a power of 2
    trace_length = 2**(ceil(log_trace_length))
    #We want the trace to be of length that is a power of two. 
    new_input = input_and_hash + [random.randrange(1, PRIME)for _ in range(4 + 12*trace_length - inp_hash_length)]
    trace_length = 32*trace_length
    p = PRIME
    trace = [[] for i in range(TRACE_SIZE)]
    state = [0] * STATE_SIZE
    inp_index = 0
    for i in range(4):
        state[i] = new_input[inp_index + i]
    inp_index += 4
    while len(trace[0]) < trace_length:
        for hash_ind in range(3):
            for i in range(4):
                state[4 + i] = new_input[inp_index + i]
                state[8 + i] = 0

            inp_index += 4
            if hash_ind == 0:
                append_state(trace, state)
            state = [(state[i] + ROUND_CONSTANTS[0][i]) % p for i in range(STATE_SIZE)]
            for round in range(NUM_ROUNDS):
                state = HalfRound(state, round*2 + 1, p)
                append_state(trace, state)
                state = HalfRound(state, round*2 + 2, p)
            if input_length <= inp_index and inp_index < input_length + 4:
            #We're right after the original hash calculation
                assert state[:4] == output, "Error in hash calculation"

        append_state(trace, state)

        assert len(trace[0]) % 32 == 0
    full_trace = []
    for i in range(len(trace[0])):
        for s in trace:
            full_trace.append(s[i])

    return full_trace

def create_rescue_polynoms(precision, output, file_hash = None):
    comp_length = precision // extension_factor

    # Root of unity such that x^precision=1
    G2 = f.exp(7, (modulus - 1) // precision)

    # Root of unity such that x^steps=1
    skips = precision // comp_length
    G1 = f.exp(G2, skips)

    #Create consts polynomial for each state_ind
    all_even_consts = []
    all_odd_consts = []
    for state_ind in range(TRACE_SIZE):
        odd_consts = []
        even_consts = []
        even_consts.append(0)
        if state_ind < STATE_SIZE:
            for j in range(HashesPerBatch):
                if state_ind < 4:
                    even_consts[-1] += ROUND_CONSTANTS[0][state_ind]
                else:
                    even_consts[-1] = ROUND_CONSTANTS[0][state_ind]
                for round in range(NUM_ROUNDS):
                    odd_consts.append(ROUND_CONSTANTS[2*round + 1][state_ind])
                    even_consts.append(ROUND_CONSTANTS[2*round + 2][state_ind])       
            even_consts.append(0)
            odd_consts.append(0)
            odd_consts.append(0)
        else:
            even_consts = [0]*BatchHeight
            odd_consts = [0]*BatchHeight
        all_even_consts.append(even_consts)
        all_odd_consts.append(odd_consts)

    all_even_next_eval = [all_even_consts[i % TRACE_SIZE][(i // TRACE_SIZE) % BatchHeight] for i in range(comp_length)]
    all_even_poly = fft(all_even_next_eval, modulus, G1, inv = True)
    all_even_eval = fft(all_even_poly, modulus, G2)
    all_odd_next_eval = [all_odd_consts[i % TRACE_SIZE][(i // TRACE_SIZE) % BatchHeight] for i in range(comp_length)]

    new_mds = [[] for i in range(TRACE_SIZE)]
    new_inv_mds = [[] for i in range(TRACE_SIZE)]
    for i in range(TRACE_SIZE):
        for j in range(TRACE_SIZE):
            if i < STATE_SIZE and j < STATE_SIZE:
                new_mds[i].append(MDS_MATRIX[i][j])
                new_inv_mds[i].append(INV_MDS_MATRIX[i][j])
            else:
                new_mds[i].append(0)
                new_inv_mds[i].append(0)  
    mds_mini = []
    inv_mds_mini = []
    for i in range(TRACE_SIZE):
        mds_mini.append([new_mds[j % TRACE_SIZE][i] for j in range(comp_length)])
        inv_mds_mini.append([new_inv_mds[j % TRACE_SIZE][i] for j in range(comp_length)])
    mds_poly = [fft(mini, modulus, G1, inv = True) for mini in mds_mini]
    inv_mds_poly = [fft(mini, modulus, G1, inv = True) for mini in inv_mds_mini]
    mds_eval = [fft(poly, modulus, G2) for poly in mds_poly]
    inv_mds_eval = [fft(poly, modulus, G2) for poly in inv_mds_poly]
    odd_consts_mod_mini = []
    for i in range(TRACE_SIZE):
        odd_consts_mod_mini.append([all_odd_next_eval[j - (j % TRACE_SIZE) + i] for j in range(comp_length)])
    odd_consts_mod_poly = [fft(mini, modulus, G1, inv = True) for mini in odd_consts_mod_mini]
    odd_consts_mod_eval = [fft(poly, modulus, G2) for poly in odd_consts_mod_poly]

    output_mini = [output[i % len(output)] for i in range(comp_length)]
    output_poly = fft(output_mini, modulus, G1, inv = True)
    output_eval = fft(output_poly, modulus, G2)

    if file_hash is not None:
        file_hash_mini = [file_hash[i % len(file_hash)] for i in range(comp_length)]
        file_hash_poly = fft(file_hash_mini, modulus, G1, inv = True)
        file_hash_eval = fft(file_hash_poly, modulus, G2)
        return all_even_eval, odd_consts_mod_eval, mds_eval, inv_mds_eval, output_eval, file_hash_eval 

    return all_even_eval, odd_consts_mod_eval, mds_eval, inv_mds_eval, output_eval, None

def rescue_sign(password, password_output, file_hash = None, constraints_powers_dict=constraints_powers_dict):
    start_time = time.time()
    full_trace = rescue_computational_trace(password, file_hash, output = password_output)
    comp_length = len(full_trace)
    input_length = len(password)
    chain_length = ceil((input_length - 4) / 4)
    precision = comp_length * extension_factor

    # Root of unity such that x^precision=1
    G2 = f.exp(7, (modulus - 1) // precision)

    # Root of unity such that x^steps=1
    skips = precision // comp_length
    G1 = f.exp(G2, skips)

    # Powers of the higher-order root of unity
    xs = get_power_cycle(G2, modulus)

    skips2 = comp_length // (BatchHeight * TRACE_SIZE)

    all_even_eval, odd_consts_mod_eval, mds_eval, inv_mds_eval, output_eval, file_hash_eval = create_rescue_polynoms(precision, password_output, file_hash)

    # Interpolate the computational trace into a polynomial P, with each step
    # along a successive power of G1
    computational_trace_polynomial = fft(full_trace, modulus, G1, inv=True)
    p_evaluations_extension = fft(computational_trace_polynomial, modulus, G2)
    print('Converted computational steps into a polynomial and low-degree extended it')
 
    p_mod_mini = []
    for i in range(TRACE_SIZE):
        p_mod_mini.append([full_trace[j - (j % TRACE_SIZE) + i] for j in range(comp_length)])
    p_mod_poly = [fft(mini, modulus, G1, inv = True) for mini in p_mod_mini]
    p_mod_eval = [fft(poly, modulus, G2) for poly in p_mod_poly]

    state_after_eval = all_even_eval[:]
    for i in range(TRACE_SIZE):
        state_after_eval = [f.add(st, f.mul(m, f.exp(p, 3))) for (st, m, p) in zip(state_after_eval, mds_eval[i], p_mod_eval[i])]


    state_before_eval = [0 for i in range(precision)]
    for i in range(TRACE_SIZE):
        subbed = [f.sub(p_mod_eval[i][(j + TRACE_SIZE * extension_factor) % precision], odd_consts_mod_eval[i][j]) for j in range(precision)]
        state_before_eval = [f.add(st, f.mul(m, su)) for (st, m, su) in zip(state_before_eval, inv_mds_eval[i], subbed)]
    state_before_eval = [f.exp(st, 3) for st in state_before_eval]



    #We compute evaluation on the extension field
    trace_plus_round0_eval = [p_evaluations_extension[i] + all_even_eval[i] for i in range(precision)]
    trace_minus_output_eval = [p_evaluations_extension[i] - output_eval[i] for i in range(precision)]
    if file_hash_eval is not None:
        trace_minus_file_hash_eval = [p_evaluations_extension[i] - file_hash_eval[i] for i in range(precision)]
    print("Computed all values polynomials")

    constraints = []
    #We enforce constraints on the state - such that 
    # 1. The trace is a true rescue computation state
    # 2. The hash of the passwords appears in the state
    # 3. The file_hash is hashed as well
    # 4. The p_mod_evals are correct

    skips3 = comp_length // TRACE_SIZE
    #This represents something that happens once every state
    once_state_eval = [xs[(i*skips3) % precision] - 1 for i in range(precision)]

    #Constraints 0 check that the last 4 bytes of every state are 0 (since we need a power of 2, but the original state is only of size 12)
    for state_ind in range(STATE_SIZE, TRACE_SIZE):
        filler_states = [once_state_eval[(i - state_ind*extension_factor)%precision] for i in range(precision)]
        filler_states_inv = f.multi_inv(filler_states)

        constraint0_evals = [f.mul(pv, fs) for (pv, fs) in zip(p_evaluations_extension, filler_states_inv)]
        constraints.append((0, constraint0_evals))
    
    #This represents something that happens once every batch
    once_batch_eval = [xs[(i*skips2) % precision] - 1 for i in range(precision)]

    #Constraints 1 check that in the beginning of each batch, bytes 8-12 are 0 (since the inital state is only of size 8) 
    for state_ind in range(8, STATE_SIZE):
        barch_ind0 = [once_batch_eval[(i - 0 * TRACE_SIZE * extension_factor - state_ind * extension_factor) %precision] for i in range(precision)]
        batch_ind0_inv = f.multi_inv(barch_ind0)

        constraint1_evals = [f.mul(pv , bi) for (pv, bi) in zip(p_evaluations_extension, batch_ind0_inv)]
        constraints.append((1, constraint1_evals))
    
    #Constraints 2 check that at the beginning of each batch, the first state is just half_state before the next one (this is a rescue demand)
    for state_ind in range(0, STATE_SIZE):
        batch_ind0 = [once_batch_eval[(i - 0 * TRACE_SIZE*extension_factor - state_ind * extension_factor) %precision] for i in range(precision)]
        batch_ind0_inv = f.multi_inv(batch_ind0)     

        constraints2_eval = [f.mul(f.sub(tpc0, stb) ,bi) for (tpc0, stb, bi) in zip(trace_plus_round0_eval, state_before_eval,  batch_ind0_inv)]
        constraints.append((2, constraints2_eval))
    
    #Constraint3 represents that for every 2 states that are not the beginning or end
    # (i % 32 != 0, 30, 31), we have state_before(next half round) = state_after(half round)
    # That's true for the first 4 bytes because:
    # a) they pass on (and not deleted in the next hash iteration)
    # b) we've fixed consts such that they already include consts[0]
    for state_ind in range(0, 4):
        batch_ind0 = [once_batch_eval[(i - 0 * TRACE_SIZE *extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind30 = [once_batch_eval[(i - 30 * TRACE_SIZE *extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind31 = [once_batch_eval[(i - 31 * TRACE_SIZE *extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        all_batches = [f.mul(f.mul(bi0, bi30),bi31) for (bi0, bi30, bi31) in zip(batch_ind0, batch_ind30, batch_ind31)]

        filler_states = [once_state_eval[(i - state_ind* extension_factor)%precision] for i in range(precision)]
        filler_states_inv = f.multi_inv(filler_states)

        constraints3_eval = [(sta - stb) * abi * fs for (sta, stb, abi, fs) in zip(state_after_eval, state_before_eval, all_batches, filler_states_inv)]
        constraints.append((3, constraints3_eval))
    
    #Constraint4 is almost as 3, but for 4:12, and that means that this condition does not apply
    # also when starting a new hash within the same batch (index 10, 20 as well)
    for state_ind in range(4, STATE_SIZE):
        batch_ind0 = [once_batch_eval[(i - 0 * TRACE_SIZE * extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind10 = [once_batch_eval[(i - 10 * TRACE_SIZE * extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind20 = [once_batch_eval[(i - 20 * TRACE_SIZE * extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind30 = [once_batch_eval[(i - 30 * TRACE_SIZE * extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind31 = [once_batch_eval[(i - 31 * TRACE_SIZE * extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        all_batches = [f.mul(f.mul(f.mul(f.mul(bi0, bi10),bi20), bi30),bi31) for (bi0, bi10 , bi20, bi30, bi31) in zip(batch_ind0, batch_ind10, batch_ind20, batch_ind30, batch_ind31)]

        filler_states = [once_state_eval[(i - state_ind * extension_factor)%precision] for i in range(precision)]
        filler_states_inv = f.multi_inv(filler_states)

        constraints4_eval = [(sta - stb) * abi * fs for (sta, stb, abi, fs) in zip(state_after_eval, state_before_eval, all_batches, filler_states_inv)]
        constraints.append((4, constraints4_eval))

    # Constraints 5 check that in the new hashes within the same batch (indexes 10, 20), bytes 8:12 are 0 (since a new hash's initial state is only 8 bytes)
    for state_ind in range(STATE_SIZE - 4, STATE_SIZE):
        batch_ind10 = [once_batch_eval[(i - 10 * TRACE_SIZE* extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch_ind20 = [once_batch_eval[(i - 20 * TRACE_SIZE* extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        all_batches = [f.mul(b10, b20) for (b10, b20) in zip(batch_ind10, batch_ind20)]
        all_batches_inv = f.multi_inv(all_batches)

        constraints5_eval = [f.sub(state_before_eval[i], all_even_eval[i]) * all_batches_inv[i] for i in range(precision)]
        constraints.append((5, constraints5_eval))

    # Constraints 6 checks that the start of the last state is just half round after the one before it.
    for state_ind in range(0, STATE_SIZE):
        batch_ind30 = [once_batch_eval[(i - 30 * TRACE_SIZE* extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch30_inv = f.multi_inv(batch_ind30)

        constraints6_eval = [(p_evaluations_extension[(i + extension_factor*TRACE_SIZE) % precision] - state_after_eval[i]) * batch30_inv[i] for i in range(precision)]
        constraints.append((6, constraints6_eval))
    
    # Constraints 7 check that the first row after a batch is the last row before the batch (since this is how we create the trace)
    for state_ind in range(0, 4):
        batch_ind31 = [once_batch_eval[(i - 31 * TRACE_SIZE* extension_factor - state_ind * extension_factor)%precision] for i in range(precision)]
        batch31_inv = f.multi_inv(batch_ind31)

        last_step_eval = [xs[i] - xs[(comp_length - TRACE_SIZE + state_ind)*extension_factor] for i in range(precision)]

        constraints7_eval = [(p_evaluations_extension[(i + extension_factor*TRACE_SIZE) % precision] - p_evaluations_extension[i]) * batch31_inv[i] * last_step_eval[i] for i in range(precision)]
        constraints.append((7, constraints7_eval))
    
    #Constraints 8 check that the password hash is actually within the trace in the right spot (this checks that we actually have a preimage of the hash)
    for state_ind in range(0, len(password_output)):
        output_row_eval = [xs[i] - xs[(ceil(chain_length/HashesPerBatch) * BatchHeight * TRACE_SIZE  - TRACE_SIZE + state_ind)*extension_factor] for i in range(precision)]
        output_row_inv = f.multi_inv(output_row_eval)

        constraints8_eval = [tmo * ori for (tmo, ori) in zip(trace_minus_output_eval, output_row_inv)]
        constraints.append((8, constraints8_eval))
    
    #This checks that p_mod_evals are actually computed properly
    for state_ind in range(0, STATE_SIZE):
        for poly_ind in range(0, STATE_SIZE):
            filler_states = [once_state_eval[(i) % precision] for i in range(precision)]
            filler_states_inv = f.multi_inv(filler_states)
            constraints9_eval = [f.mul(f.sub(p_evaluations_extension[(i + extension_factor*poly_ind) % precision] ,p_mod_eval[poly_ind][(i + state_ind*extension_factor) % precision]), filler_states_inv[i]) for i in range(precision)]
            constraints.append((9, constraints9_eval))

    #The last constraints check that the file_hash appears within the computational trace in the place it should appear in. 
    if file_hash is not None:
        for state_ind in range(4, 8):
            file_hash_row_eval = [xs[i] - xs[(ceil(chain_length/HashesPerBatch) * BatchHeight * TRACE_SIZE + BatchHeight*TRACE_SIZE*RAND_BEFORE + state_ind)*extension_factor] for i in range(precision)]
            file_hash_row_inv = f.multi_inv(file_hash_row_eval)

            constraints10_eval = [tmo * ori for (tmo, ori) in zip(trace_minus_file_hash_eval, file_hash_row_inv)]
            constraints.append((10, constraints10_eval))
    print("Computed all constraints polynomials")


    #We create merkel trees for the p's and c's (trace polynomials and constraints polynomials)
    p_eval_bytes = [x.to_bytes(8, 'big') for x in p_evaluations_extension]
    p_mod_eval_bytes = [[x.to_bytes(8, 'big') for x in p_mod_i] for p_mod_i in p_mod_eval]
    p_values_bytes = [p_eval_bytes[i] + b"".join([p[i] for p in p_mod_eval_bytes]) for i in range(precision)]
    p_mtree = merkelize(p_values_bytes)
    constraints_bytes = [[(x % modulus).to_bytes(8,'big') for x in constraint] for _, constraint in constraints]
    constraints_concat_bytes = [b"".join([c[i] for c in constraints_bytes]) for i in range(precision)]
    c_mtree = merkelize(constraints_concat_bytes)
    print("Computed hash roots")

    #We generate a linear combination of those polynomials, deg adjusted, with random constants
    ks = []
    for i in range(2*(len(constraints) + len(p_mod_eval)) + 2):
        ks.append(int.from_bytes(blake(p_mtree[1] + i.to_bytes(2, 'big')), 'big') % modulus)

    total_power = comp_length*6
    #toatl_power - deg(constraint) for each constraint type
    #We also add the total_power - def(p) or p_mod (which is comp_length) for them at the end
    powers_list = [constraints_powers_dict[ind](total_power, comp_length) for ind, _ in constraints] + [total_power - comp_length for i in range(len(p_mod_eval) + 1)]
    powers_eval = []
    for power in powers_list:
        G2_to_the_power = f.exp(G2, power)
        tmp_powers = [1]
        for i in range(1, precision):
            tmp_powers.append(tmp_powers[-1]*G2_to_the_power % modulus)
        powers_eval.append(tmp_powers)
        
    l_evaluations = [0 for i in range(precision)]
    #We add all the constraints, deg adjusted
    for c_ind, (_, constraint) in enumerate(constraints):
        #l += (k[2*c_ind] + k[2*c_ind + 1]*g**constraint_power) * constraint
        l_evaluations = [f.add(l_evaluations[i], f.mul(f.add(ks[c_ind*2], f.mul(ks[c_ind*2 + 1], powers_eval[c_ind][i])), constraint[i])) for i in range(precision)]
    num_constraints = NUM_CONSTRAINTS
    if file_hash is not None:
        num_constraints += 4
    assert num_constraints == len(constraints) 
        
    #We add all the p_mod values, deg adjusted
    for p_ind, p_mod_i in enumerate(p_mod_eval):
        l_evaluations = [f.add(l_evaluations[i], f.mul(f.add(ks[2*num_constraints + p_ind*2], f.mul(ks[2*num_constraints + p_ind*2 + 1], powers_eval[num_constraints + p_ind][i])), p_mod_i[i])) for i in range(precision)]
    #We add p_evaluations, deg adjusted
    l_evaluations = [f.add(l_evaluations[i], f.mul(f.add(ks[-2], f.mul(ks[-1], powers_eval[-1][i])), p_evaluations_extension[i])) for i in range(precision)]


    l_mtree = merkelize(l_evaluations)
    print("Computed random linear combination")

    # Do some spot checks of the Merkle tree at pseudo-random coordinates, excluding
    # multiples of `extension_factor`
    samples = spot_check_security_factor
    positions = get_pseudorandom_indices(l_mtree[1], precision, samples,
                                         exclude_multiples_of=extension_factor)
    augmented_positions = sum([[(x - ((x // extension_factor) % TRACE_SIZE)* extension_factor + i*extension_factor) % precision for i in range(2*TRACE_SIZE)] for x in positions], [])
    print('Computed %d spot checks' % samples)

    # Return the Merkle roots of P and D, the spot check Merkle proofs,
    # and low-degree proofs of P and D
    low_degree_pf = prove_low_degree(l_evaluations, G2, total_power, modulus, exclude_multiples_of=extension_factor)

    o = [p_mtree[1],
         c_mtree[1],
         l_mtree[1],
         mk_multi_branch(p_mtree, augmented_positions),
         mk_multi_branch(c_mtree, augmented_positions),
         mk_multi_branch(l_mtree, augmented_positions),
         low_degree_pf]
    print("STARK computed in %.4f sec" % (time.time() - start_time))
    assert verify_low_degree_proof(l_mtree[1], G2, low_degree_pf, total_power, modulus, exclude_multiples_of=extension_factor), "Couldn't verify low_degree pf"
    return o

# Verifies a STARK
def rescue_verify(output, proof, file_hash = None, chain_length = 12, comp_length = 4096):
    p_root, c_root, l_root, p_branches, c_branches,  linear_comb_branches, fri_proof = proof
    start_time = time.time()
    if not is_a_power_of_2(comp_length):
        return False

    precision = comp_length * extension_factor

    # Get (steps)th root of unity
    G2 = f.exp(7, (modulus-1)//precision)
    skips2 = comp_length // (BatchHeight * TRACE_SIZE)
    skips3 = comp_length // TRACE_SIZE


    total_power = comp_length * 6
    if not verify_low_degree_proof(l_root, G2, fri_proof, total_power, modulus, exclude_multiples_of=extension_factor):
        return False
    print("Verified the random linear combination is low degree")
    all_even_eval, odd_consts_mod_eval, mds_eval, inv_mds_eval, output_eval, file_hash_eval = create_rescue_polynoms(precision, output, file_hash)

    num_constraints = NUM_CONSTRAINTS
    if file_hash is not None:
        num_constraints += 4
    powers = get_power_list(total_power, comp_length, file_hash is not None)
    # Performs the spot checks
    ks = []
    for i in range(2*(num_constraints + TRACE_SIZE) + 2):
        ks.append(int.from_bytes(blake(p_root + i.to_bytes(2, 'big')), 'big') % modulus)

    samples = spot_check_security_factor
    positions = get_pseudorandom_indices(l_root, precision, samples,
                                         exclude_multiples_of=extension_factor)
    augmented_positions = sum([[(x - ((x // extension_factor) % TRACE_SIZE)* extension_factor + i*extension_factor) % precision for i in range(2*TRACE_SIZE)] for x in positions], [])
    p_branch_leaves = verify_multi_branch(p_root, augmented_positions, p_branches)
    c_branch_leaves = verify_multi_branch(c_root, augmented_positions, c_branches)
    linear_comb_branch_leaves = verify_multi_branch(l_root, augmented_positions, linear_comb_branches)
    print("Verified Merkle branches")
    for i, pos in enumerate(positions):
        p_branches = [p_branch_leaves[i*(2*TRACE_SIZE) + j] for j in range(2*TRACE_SIZE)]
        p_vals = []
        p_mod_vals = [[] for j in range(TRACE_SIZE)]
        for j in range(2*TRACE_SIZE):
            p_vals.append(int.from_bytes(p_branches[j][:8], 'big'))
            for k in range(TRACE_SIZE):
                p_mod_vals[k].append(int.from_bytes(p_branches[j][8 + 8*k : 16 + 8*k], 'big'))
        for pos_ind in range(TRACE_SIZE):
            l_res = 0
            pos = pos - ((pos // extension_factor) % TRACE_SIZE)*extension_factor + pos_ind * extension_factor
            x = f.exp(G2, pos)
            c_branch = c_branch_leaves[i*(2*TRACE_SIZE) + pos_ind]
            #Calculate the values of all the polynomials
            l_of_x = int.from_bytes(linear_comb_branch_leaves[i*(2*TRACE_SIZE) + pos_ind], 'big')
            if not pos_ind == (pos // extension_factor) % TRACE_SIZE:
                return False
            c_vals = []
            for j in range(0, len(c_branch)// 8):
                c_vals.append(int.from_bytes(c_branch[8*j : 8 + 8*j], 'big'))
                l_res += c_vals[-1] * (ks[j*2 + 0]+ ks[j*2 + 1] * f.exp(x, powers[j]))

            state_after_eval = all_even_eval[pos]
            for j in range(TRACE_SIZE):
                state_after_eval = f.add(state_after_eval, f.mul(mds_eval[j][pos], f.exp(p_mod_vals[j][pos_ind], 3)))
            state_before_eval = 0
            for j in range(TRACE_SIZE):
                subbed = f.sub(p_mod_vals[j][pos_ind + TRACE_SIZE], odd_consts_mod_eval[j][pos])
                state_before_eval = f.add(state_before_eval, f.mul(inv_mds_eval[j][pos], subbed))
            state_before_eval = f.exp(state_before_eval, 3) 

            #Validate the constraints:
            const_ind = 0
            const_type_ind = 0
            for state_ind in range(STATE_SIZE, TRACE_SIZE):
                filler_state = f.sub(f.exp(G2, skips3 * (pos - state_ind*extension_factor) % precision), 1)

                if not c_vals[const_ind] == f.div(p_vals[pos_ind], filler_state):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1

            const_type_ind += 1
            for state_ind in range(8, STATE_SIZE):
                batch_ind0 = f.sub(f.exp(G2, skips2*(pos - 0 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)

                if not c_vals[const_ind] == f.div(p_vals[pos_ind], batch_ind0):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1
            
            const_type_ind += 1
            for state_ind in range(0, STATE_SIZE):
                batch_ind0 = f.sub(f.exp(G2, skips2*(pos - 0 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                if not c_vals[const_ind] == f.div(f.sub(f.add(p_vals[pos_ind], all_even_eval[pos]), state_before_eval), batch_ind0):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1
            
            const_type_ind += 1
            for state_ind in range(0, 4):
                batch_ind0 = f.sub(f.exp(G2, skips2*(pos - 0 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind30 = f.sub(f.exp(G2, skips2*(pos - 30 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind31 = f.sub(f.exp(G2, skips2*(pos - 31 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                all_batches = f.mul(f.mul(batch_ind0, batch_ind30),batch_ind31) 

                filler_state = f.sub(f.exp(G2, skips3 * (pos - state_ind*extension_factor) % precision), 1)

                if not c_vals[const_ind] == f.div(f.mul(f.sub(state_after_eval, state_before_eval), all_batches), filler_state):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1        
            
            const_type_ind += 1
            for state_ind in range(4, STATE_SIZE):
                batch_ind0 = f.sub(f.exp(G2, skips2*(pos - 0 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind10 = f.sub(f.exp(G2, skips2*(pos - 10 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind20 = f.sub(f.exp(G2, skips2*(pos - 20 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind30 = f.sub(f.exp(G2, skips2*(pos - 30 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind31 = f.sub(f.exp(G2, skips2*(pos - 31 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                all_batches = f.mul(f.mul(f.mul(f.mul(batch_ind0, batch_ind10), batch_ind20), batch_ind30),batch_ind31) 

                filler_state = f.sub(f.exp(G2, skips3 * (pos - state_ind*extension_factor) % precision), 1)

                if not c_vals[const_ind] == f.div(f.mul(f.sub(state_after_eval, state_before_eval), all_batches), filler_state):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1
            
            const_type_ind += 1
            for state_ind in range(STATE_SIZE - 4, STATE_SIZE):
                batch_ind10 = f.sub(f.exp(G2, skips2*(pos - 10 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                batch_ind20 = f.sub(f.exp(G2, skips2*(pos - 20 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                all_batches = f.mul(batch_ind10, batch_ind20)

                if not c_vals[const_ind] == f.div(f.sub(state_before_eval, all_even_eval[pos]), all_batches):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1

            const_type_ind += 1
            for state_ind in range(0, STATE_SIZE):
                batch_ind30 = f.sub(f.exp(G2, skips2*(pos - 30 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)

                if not c_vals[const_ind] == f.div(f.sub(p_vals[pos_ind + TRACE_SIZE], state_after_eval), batch_ind30):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1

            const_type_ind += 1
            for state_ind in range(0, 4):
                batch_ind31 = f.sub(f.exp(G2, skips2*(pos - 31 * TRACE_SIZE * extension_factor - state_ind*extension_factor) % precision), 1)
                last_step_eval = x - f.exp(G2, (comp_length - TRACE_SIZE + state_ind) *extension_factor)  

                if not c_vals[const_ind] == f.div(f.mul(f.sub(p_vals[pos_ind + TRACE_SIZE], p_vals[pos_ind]), last_step_eval), batch_ind31):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1

            const_type_ind += 1
            for state_ind in range(0, len(output)):
                output_row_eval = f.sub(x, f.exp(G2, (ceil(chain_length/HashesPerBatch) * BatchHeight * TRACE_SIZE  - TRACE_SIZE + state_ind)*extension_factor))
                
                if not c_vals[const_ind] == f.div(f.sub(p_vals[pos_ind], output_eval[pos]), output_row_eval):
                    print(f"Failed in Constraints {const_type_ind}")
                    return False
                const_ind += 1

            const_type_ind += 1
            for state_ind in range(0, STATE_SIZE):
                for poly_ind in range(0, STATE_SIZE):
                    filler_state = f.sub(f.exp(G2, skips3 * (pos)), 1)

                    if not c_vals[const_ind] == f.div(f.sub(p_vals[pos_ind + poly_ind], p_mod_vals[poly_ind][pos_ind + state_ind]), filler_state):
                        print(f"Failed in Constraints {const_type_ind}")
                        return False
                    const_ind += 1
            
            if file_hash is not None:
                const_type_ind += 1
                for state_ind in range(4, 8):
                    file_hash_row_eval = f.sub(x, f.exp(G2, (ceil(chain_length/HashesPerBatch) * BatchHeight * TRACE_SIZE + BatchHeight*TRACE_SIZE*RAND_BEFORE + state_ind)*extension_factor))
                    
                    if not c_vals[const_ind] == f.div(f.sub(p_vals[pos_ind], file_hash_eval[pos]), file_hash_row_eval):
                        print(f"Failed in Constraints {const_type_ind}")
                        return False
                    const_ind += 1

            #We add all the p_mod values, deg adjusted
            for p_ind, p_mod_i in enumerate(p_mod_vals):
                l_res = f.add(l_res, f.mul(f.add(ks[2*num_constraints + p_ind*2], f.mul(ks[2*num_constraints + p_ind*2 + 1], f.exp(x, powers[num_constraints + p_ind]))), p_mod_i[pos_ind]))
            #We add p_evaluations, deg adjusted
            l_res  = f.add(l_res, f.mul(f.add(ks[-2], f.mul(ks[-1], f.exp(x, powers[num_constraints + TRACE_SIZE]))), p_vals[pos_ind]))
            # Check correctness of the linear combination
            if not (l_of_x == l_res):
                print("Linear combination is not correct")
                return False

    print('Verified %d consistency checks' % (TRACE_SIZE * spot_check_security_factor))
    print('Verified STARK in %.4f sec' % (time.time() - start_time))
    return True
