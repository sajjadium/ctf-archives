import os
import random

from Crypto.Util.number import inverse

# RSA public parameters
# Corrected modulus n = p * q
p = None # Hidden
q = None # Hidden
n = 30392456691103520456566703629789883376981975074658985351907533566054217142999128759248328829870869523368987496991637114688552687369186479700671810414151842146871044878391976165906497019158806633675101
e = 65537

# Encrypted flag
flag = os.environ.get("FLAG", "flag{not_the_real_flag}")
flag_int = int.from_bytes(flag.encode(), 'big')
flag_bytes = flag.encode()
flag_length = len(flag_bytes)
ciphertext = pow(flag_int, e, n)

# Ensure n is correct
assert p * q == n

phi = (p - 1) * (q - 1)
d = inverse(e, phi)

dP = d % (p - 1)
dQ = d % (q - 1)
qInv = inverse(q, p)

def decrypt(c_hex):
    try:
        c = int(c_hex, 16)
    except ValueError:
        return None, False, "Invalid ciphertext format. Please provide hexadecimal digits."
    if c >= n:
        return None, False, "Ciphertext must be less than modulus n."
    if c == ciphertext:
        return None, False, "Can't use the flag!"

    # Simulate fault occurrence
    faulty = random.randint(1, 10) == 1  # Fault occurs 1 in 10 times

    # Decrypt using CRT
    m1 = pow(c, dP, p)
    m2 = pow(c, dQ, q)
    if faulty:
        # Introduce fault in m1
        m1 = random.randrange(1, p)
    # Combine using CRT
    h = (qInv * (m1 - m2)) % p
    m = (m2 + h * q) % n
    return m, faulty, None


def main():
    print("Welcome to the RSA Decryption Oracle!")
    print("You can decrypt your own ciphertexts.")
    print("Retrieve the encrypted flag to get the secret message.")
    print("Type 'flag' to get the encrypted flag.")
    print("Type 'exit' to quit.")
    while True:
        print("\nSend your ciphertext in hex format:")
        c_hex = input().strip()
        if not c_hex:
            break
        if c_hex.lower() == 'exit':
            print("Goodbye!")
            break
        elif c_hex.lower() == 'flag':
            print(f"Encrypted flag (hex): {hex(ciphertext)}")
            print(f"Flag length (bytes): {flag_length}")
            continue
        m, faulty, error = decrypt(c_hex)
        if error:
            print(error)
        else:
            print(f"Decrypted message (hex): {hex(m)}")
            if faulty:
                print("Note: Fault occurred during decryption.")


if __name__ == "__main__":
    main()
