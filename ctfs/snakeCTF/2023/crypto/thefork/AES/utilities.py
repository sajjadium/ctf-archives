from AES.data import *

def shift_rows(current_state):
    output = [0 for _ in range(16)]


    for i in range(0,4):
        for j in range(4):
            output[j+4*i] = (current_state[j+((j+i)*4)%16])
    return output

def inverse_shift_row(current_state):
    output = [0 for _ in range(16)]
    
    for i in range(0,4):
        for j in range(4):
            output[j+4*i] = (current_state[j+((i+(4-j))*4)%16])
    return output

def mix_columns(current_state):
    output = []
    for i in range(4):
        output.append((mul2[current_state[(4*i)+0]] ^ mul_3[current_state[(4*i)+1]] ^ current_state[(4*i)+2] ^ current_state[(4*i)+3]) & 255)
        output.append((current_state[(4*i)+0] ^ mul2[current_state[(4*i)+1]] ^ mul_3[current_state[(4*i)+2]] ^ current_state[(4*i)+3]) & 255)
        output.append((current_state[(4*i)+0] ^ current_state[(4*i)+1] ^ mul2[current_state[(4*i)+2]] ^ mul_3[current_state[(4*i)+3]]) & 255)
        output.append((mul_3[current_state[(4*i)+0]] ^ current_state[(4*i)+1] ^ current_state[(4*i)+2] ^ mul2[current_state[(4*i)+3]]) & 255)
    return output

def inverse_mix_columns(current_state):
    output = []
    for i in range(4):
        output.append((mul_14[current_state[(4*i)+0]] ^ mul_11[current_state[(4*i)+1]] ^ mul_13[current_state[(4*i)+2]] ^ mul_9[current_state[(4*i)+3]]) & 255)
        output.append((mul_9[current_state[(4*i)+0]] ^ mul_14[current_state[(4*i)+1]] ^ mul_11[current_state[(4*i)+2]] ^ mul_13[current_state[(4*i)+3]]) & 255)
        output.append((mul_13[current_state[(4*i)+0]] ^ mul_9[current_state[(4*i)+1]] ^ mul_14[current_state[(4*i)+2]] ^ mul_11[current_state[(4*i)+3]]) & 255)
        output.append((mul_11[current_state[(4*i)+0]] ^ mul_13[current_state[(4*i)+1]] ^ mul_9[current_state[(4*i)+2]] ^ mul_14[current_state[(4*i)+3]]) & 255)
    return output

def add(current_state, item):
    output = []
    for i in range(16):
        output.append(current_state[i] ^ item[i])
    return output

def sub_bytes(current_state):
    output = []
    for i in range(16):
        output.append(SBOX[current_state[i]])
    
    return output

def inverse_sub_bytes(current_state):
    output = []
    for i in range(16):
        output.append(INV_SBOX[current_state[i]])
    
    return output

def key_expansion(key, total_rounds):
    keys = [ [] for i in range(total_rounds)]

    # K0 = Key
    for i in range(16):
        keys[0].append(key[i])

    for i in range(1,total_rounds):
        keys[i].append(SBOX[ keys[i-1][13] ] ^ keys[i-1][0] ^ Rcon[ i ])
        keys[i].append(SBOX[ keys[i-1][14] ] ^ keys[i-1][1])
        keys[i].append(SBOX[ keys[i-1][14] ] ^ keys[i-1][2])
        keys[i].append(SBOX[ keys[i-1][12] ] ^ keys[i-1][3])

        keys[i].append(keys[i-1][4] ^ keys[i][0])
        keys[i].append(keys[i-1][5] ^ keys[i][1])
        keys[i].append(keys[i-1][6] ^ keys[i][2])
        keys[i].append(keys[i-1][7] ^ keys[i][3])

        keys[i].append(keys[i-1][8] ^ keys[i][4])
        keys[i].append(keys[i-1][9] ^ keys[i][5])
        keys[i].append(keys[i-1][10] ^ keys[i][6])
        keys[i].append(keys[i-1][11] ^ keys[i][7])

        keys[i].append(keys[i-1][12] ^ keys[i][8])
        keys[i].append(keys[i-1][13] ^ keys[i][9])
        keys[i].append(keys[i-1][14] ^ keys[i][10])
        keys[i].append(keys[i-1][15] ^ keys[i][11])

    return keys