from flag import FLAG
import secrets

def share_bits_with_you(flag):
    # Convert the flag to its binary representation
    flag_bits = ''.join(f'{ord(c):08b}' for c in flag)
    num_bits = len(flag_bits)
    indices = list(range(num_bits))
    
    # Fisher-Yates shuffle to mix up the bits
    for i in range(num_bits - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        indices[i], indices[j] = indices[j], indices[i]
    
    # Split the bits: half for you, half for me :3
    boyfriend_indices = indices[:num_bits // 2]
    my_indices = indices[num_bits // 2:]
    
    flipped_bits = list(flag_bits)
    # You get your bits unchanged
    for i in boyfriend_indices:
        flipped_bits[i] = flag_bits[i]
    # I keep my bits by flipping them, keeping them secret (tehe~)
    for i in my_indices:
        flipped_bits[i] = '1' if flag_bits[i] == '0' else '0'
    
    # Combine the bits back into a string
    flipped_flag = ''.join(flipped_bits)
    # Convert the binary string to hexadecimal
    hex_result = hex(int(flipped_flag, 2))[2:]
    # Pad the hex result with zeros to ensure it matches the correct number of bits
    hex_result = hex_result.zfill((num_bits + 3) // 4)
    return hex_result

# Share the bits 1000000 times <3 <3 <3
for _ in range(1000000):
    result = share_bits_with_you(FLAG)
    print(result)