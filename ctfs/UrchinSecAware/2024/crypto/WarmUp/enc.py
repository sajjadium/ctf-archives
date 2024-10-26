from sympy import mod_inverse

def generate_knapsack():
    knapsack = [1, 2]
    for i in range(6):
        knapsack.append(sum(knapsack) + 1)
    return knapsack

def convert_to_bits(message):
    bits = []
    for char in message:
        char_bits = bin(ord(char))[2:].zfill(8)
        bits.extend([int(b) for b in char_bits])
    return bits

def encrypt_message(message, knapsack, m, n):
    bits = convert_to_bits(message)
    chunk_size = len(knapsack)
    chunks = [bits[i:i + chunk_size] for i in range(0, len(bits), chunk_size)]
    ciphertext = []
    for chunk in chunks:
        if len(chunk) < chunk_size:
            chunk += [0] * (chunk_size - len(chunk))
        c_value = sum(k * b for k, b in zip(knapsack, chunk))
        encrypted_value = (c_value * n) % m
        ciphertext.append(encrypted_value)
    return ciphertext

if __name__ == "__main__":
    message = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    knapsack = generate_knapsack()
    m = 257
    n = random.randint(-1000, 1000)
    ciphertext = encrypt_message(message, knapsack, m, n)
    print("Ciphertext:", ciphertext)