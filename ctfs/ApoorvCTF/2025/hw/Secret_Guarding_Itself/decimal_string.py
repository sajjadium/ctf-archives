def dec_to_string(dec):
    binary = str(bin(dec)).replace("b","")
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text