from pwn import xor

Rcon = ["01000000", "02000000", "04000000", "08000000", "10000000", 
        "20000000", "40000000", "80000000", "1b000000", "36000000"]

def SubWord(word):
    return word

def RotWord(word):
    return word[2:] + word[:2]

def KeyExpansion(key):
    w = [key[i:i+8] for i in range(0, 32, 8)]
    w += [0] * 40

    for i in range(4, 44):
        temp = w[i - 1]
        if i % 4 == 0:
            temp = xor(bytes.fromhex(SubWord(RotWord(temp))), 
                       bytes.fromhex(Rcon[(i // 4) - 1])).hex()
        w[i] = xor(bytes.fromhex(w[i - 4]), bytes.fromhex(temp)).hex()
    
    return w 

def GenerateRoundKeys(w):
    round_keys = [0] * 11
    for r in range(0, 11):
        round_keys[r] = ''.join(w[4*r:4*(r+1)])
    
    return round_keys

def ToMatrix(hexstring):
    matrix = [[0] * 4 for _ in range(4)]

    for i in range(0, 32, 2):
        index = i // 2
        row = index % 4
        col = index // 4
        matrix[row][col] = hexstring[i:i+2]
    
    return matrix

def FromMatrix(matrix):
    hexstring = ""
    for j in range(4):
        for i in range(4):
            hexstring += matrix[i][j]
    
    return hexstring

def AddRoundKey(state, round_key):
    state = FromMatrix(state)
    state = xor(bytes.fromhex(state), bytes.fromhex(round_key)).hex()
    state = ToMatrix(state)

    return state

def SubBytes(state):
    return state

def ShiftRows(state):
    state[1][0], state[1][1], state[1][2], state[1][3] = state[1][1], state[1][2], state[1][3], state[1][0]
    state[2][0], state[2][1], state[2][2], state[2][3] = state[2][2], state[2][3], state[2][0], state[2][1]
    state[3][0], state[3][1], state[3][2], state[3][3] = state[3][3], state[3][0], state[3][1], state[3][2]

    return state

def GMul(a, b):
    b = int(b, 16)
    p = 0
    for c in range(8):
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11b
        b>>=1
    return p

def MixColumns(state):
    temp_state = [[0] * 4 for _ in range(4)]

    for j in range(4):
        temp_state[0][j] = hex(GMul(0x02, state[0][j]) ^ GMul(0x03, state[1][j]) ^ int(state[2][j], 16) ^ int(state[3][j], 16))[2:].zfill(2)
        temp_state[1][j] = hex(int(state[0][j], 16) ^ GMul(0x02, state[1][j]) ^ GMul(0x03, state[2][j]) ^ int(state[3][j], 16))[2:].zfill(2)
        temp_state[2][j] = hex(int(state[0][j], 16) ^ int(state[1][j], 16) ^ GMul(0x02, state[2][j]) ^ GMul(0x03, state[3][j]))[2:].zfill(2)
        temp_state[3][j] = hex(GMul(0x03, state[0][j]) ^ int(state[1][j], 16) ^ int(state[2][j], 16) ^ GMul(0x02, state[3][j]))[2:].zfill(2)
    
    for i in range(4):
        for j in range(4):
            state[i][j] = temp_state[i][j]
    
    return state
    
def AES_128(x, round_keys):
    state = ToMatrix(x)
    state = AddRoundKey(state, round_keys[0])
    for r in range(1, 10):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, round_keys[r])

    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, round_keys[10])
    state = FromMatrix(state)
    y = state
    return y

if __name__ == '__main__':
    with open('gaslight-newjeans-is-five/info.txt', 'r') as file:
        master_key = file.readline().strip()
        flag = file.readline().strip()

    w = KeyExpansion(master_key)
    round_keys = GenerateRoundKeys(w)
    
    pt1 = "696e636f6d70726568656e7369626c65"
    flag = flag.encode().hex()

    print(AES_128(pt1, round_keys))
    print(AES_128(flag, round_keys))