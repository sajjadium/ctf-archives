def binary_encode_message(message: int, N_bits: int):
    bit_list = []
    for i in range(N_bits):
        bit_list.append((message>>i) & 0x1)
    return bit_list

def decode_message(encoded_message: list, p: int):
    m = 0
    threshold = 2 if(p == 2) else ((p+1)>>1)
    for i,c in enumerate(encoded_message):
        if c >= threshold:
            c = -(p-c)
        else:
            c = c
        m = (m + (c * pow(2,i)))
    return m
