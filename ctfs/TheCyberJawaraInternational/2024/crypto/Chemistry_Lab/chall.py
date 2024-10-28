import numpy as np
from random import *
from PIL import Image


dna_rules = {
    1: {'00': 'A', '11': 'T', '01': 'G', '10': 'C'},
    2: {'00': 'A', '11': 'T', '10': 'G', '01': 'C'},
    3: {'01': 'A', '10': 'T', '00': 'G', '11': 'C'},
    4: {'01': 'A', '10': 'T', '11': 'G', '00': 'C'},
    5: {'10': 'A', '01': 'T', '00': 'G', '11': 'C'},
    6: {'10': 'A', '01': 'T', '11': 'G', '00': 'C'},
    7: {'11': 'A', '00': 'T', '01': 'G', '10': 'C'},
    8: {'11': 'A', '00': 'T', '10': 'G', '01': 'C'}
}

def dna_encode_matrix(P, rule_number):
    rule = dna_rules[rule_number]
    dna_encoded_rows = []
    for row in P:
        dna_row = []
        for num in row:
            binary_str = f'{num:08b}'
            for i in range(0, 8, 2):
                bit_pair = binary_str[i:i+2]
                dna_row.append(rule[bit_pair])
        dna_encoded_rows.append(dna_row)
    return np.array(dna_encoded_rows)

def dna_decode_matrix(dna_matrix, rule_number):
    rule = dna_rules[rule_number]
    rev_rule = {v: k for k, v in rule.items()}
    decoded_rows = []
    for row in dna_matrix:
        bit_pairs = [rev_rule.get(base, '00') for base in row]
        num_bits = ''.join(bit_pairs)
        num_bytes = len(num_bits) // 8
        decoded_row = [int(num_bits[i*8:(i+1)*8], 2) for i in range(num_bytes)]
        decoded_rows.append(decoded_row)
    return np.array(decoded_rows, dtype=np.uint8)

def xor_matrices(matrix1, matrix2, rule_number):
    rule = dna_rules[rule_number]
    rev_rule = {v: k for k, v in rule.items()}
    xor_rows = []
    for row1, row2 in zip(matrix1, matrix2):
        xor_row = []
        for b1, b2 in zip(row1, row2):
            bits1 = rev_rule[b1]
            bits2 = rev_rule[b2]
            xor_bits = format(int(bits1, 2) ^ int(bits2, 2), '02b')
            xor_row.append(rule[xor_bits])
        xor_rows.append(xor_row)
    return np.array(xor_rows)

def scramble_matrix(P, lx, ly):
    return P[lx, :][:, ly]

def generate_matrix(x, y):
    return np.frombuffer(randbytes(x * y), dtype=np.uint8).reshape((x, y))

def generate_sequence(n):
    l = list(range(n))
    for i in range(n):
        j = randint(i, n-1)
        l[i], l[j] = l[j], l[i]
    return np.array(l)

def adjust_sequences(seq, new_length):
    filtered_seq = seq[seq < new_length]
    repeats = -(-new_length // len(filtered_seq))
    return np.tile(filtered_seq, repeats)[:new_length]

def parse_user_input(user_input):
    try:
        rows = user_input.strip().split(';')
        matrix = []
        num_columns = None
        for row in rows:
            elements = list(map(int, row.strip().split(',')))
            if not all(0 <= elem <= 255 for elem in elements):
                raise ValueError
            if num_columns is None:
                num_columns = len(elements)
            elif len(elements) != num_columns:
                raise ValueError
            matrix.append(elements)
        return np.array(matrix, dtype=np.uint8)
    except:
        raise ValueError("Invalid input.")

if __name__ == "__main__":
    img = Image.open('flag.png').convert('L')
    img_data = np.array(img)
    width, height = img.size
    rule_number = 3
    dna_encoded_flag = dna_encode_matrix(img_data, rule_number)

    formula = generate_matrix(height,width)
    dna_encoded_formula = dna_encode_matrix(formula, rule_number)
    lx, ly = generate_sequence(height), generate_sequence(4*width)
    total_bases = dna_encoded_formula.size

    print("Welcome to the Chemistry Lab!\nToday we will learn about DNA Encryption for Images.\n")   
    for _ in range(5):
        print("Which experiment would you like to try?\n1. Get encrypted formula\n2. Get encrypted input\n3. Get encrypted flag")
        experiment = input()

        if experiment == "1":
            scrambled_formula = scramble_matrix(dna_encoded_formula, lx, ly)
            keystream = dna_encode_matrix(generate_matrix(height,width), 7).flatten()
            key_matrix = keystream.reshape(dna_encoded_formula.shape)
            formula_enc = xor_matrices(scrambled_formula, key_matrix, rule_number)
            decoded_formula_enc = dna_decode_matrix(formula_enc, 4)
            encrypted_formula = ';'.join(','.join(map(str, row)) for row in decoded_formula_enc)
            print("Encrypted formula:")
            print(encrypted_formula)

        if experiment == "2":
            user_input = input(f"What do you want to encrypt? ")
            try:
                user_matrix = parse_user_input(user_input)
                dna_encoded_user = dna_encode_matrix(user_matrix, rule_number)

                total_bases_user = dna_encoded_user.size
                repeats_key = -(-total_bases_user // total_bases)
                keystream = dna_encode_matrix(generate_matrix(height,width), 7).flatten()
                extended_keystream = np.tile(keystream, repeats_key)[:total_bases_user]
                extended_key_matrix = extended_keystream.reshape(dna_encoded_user.shape)
                data_rows, data_cols = dna_encoded_user.shape
                lx_user = adjust_sequences(lx, data_rows)
                ly_user = adjust_sequences(ly, data_cols)

                scrambled_user = scramble_matrix(dna_encoded_user, lx_user, ly_user)
                result_dna = xor_matrices(scrambled_user, extended_key_matrix, rule_number)
                result_decoded = dna_decode_matrix(result_dna, 4)
                encrypted_input = ';'.join(','.join(map(str, row)) for row in result_decoded)
                print("Encrypted input:")
                print(encrypted_input)
            except ValueError:
                print("Invalid input.")
                continue

        if experiment == "3":
            plaintext_input = input("What is the plaintext of the Formula? ")
            try:
                plaintext_matrix = parse_user_input(plaintext_input)
                if np.array_equal(plaintext_matrix, formula):
                    print("Congrats, here is the pixel data of flag.png encrypted with the same set of secrets used to encrypt Formula")
                    scrambled_flag = scramble_matrix(dna_encoded_flag, lx, ly)
                    flag_enc = xor_matrices(scrambled_flag, key_matrix, rule_number)
                    decoded_flag_enc = dna_decode_matrix(flag_enc, 4)
                    encrypted_flag = ';'.join(','.join(map(str, row)) for row in decoded_flag_enc)
                    print(encrypted_flag)
                else:
                    print("Incorrect plaintext.")
            except ValueError:
                print("Invalid input.")

    print("Ding Ding Ding... The bell is ringing. Time for the next class!")
