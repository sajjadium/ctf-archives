from Crypto.Cipher import AES

def decrypt_with_aes(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext.rstrip(b'\0')

def main():
    # Read the ciphertext from the file
    with open("ciphertext.txt", "rb") as f:
        ciphertext = f.read()

    # Get the key from user input
    key_str = input("Enter the key: ").strip()  # Strip leading and trailing whitespace
    try:
        # Convert the string key to bytes
        key = int(key_str).to_bytes(16, byteorder='big')  # Convert to bytes using int.to_bytes()
    except ValueError:
        print("Invalid key format. Please enter a valid integer key.")
        return

    # Decrypt the ciphertext using the key
    decrypted_ciphertext = decrypt_with_aes(key, ciphertext)
    print("Decrypted plaintext:", decrypted_ciphertext.decode())

if __name__ == "__main__":
    main()
