#!/usr/bin/env python3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def aes_cbc_encrypt(msg: bytes, key: bytes) -> bytes:
    """
    Encrypts a message using AES in CBC mode.
    
    Parameters:
        msg (bytes): The plaintext message to encrypt.
        key (bytes): The encryption key (must be 16, 24, or 32 bytes long).
    
    Returns:
        bytes: The initialization vector (IV) concatenated with the encrypted ciphertext.
    """
    if len(key) not in {16, 24, 32}:
        raise ValueError("Key must be 16, 24, or 32 bytes long.")

    # Generate a random Initialization Vector (IV)
    iv = os.urandom(16)

    # Pad the message to be a multiple of the block size (16 bytes for AES)
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_msg = padder.update(msg) + padder.finalize()

    # Create the AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded message
    ciphertext = encryptor.update(padded_msg) + encryptor.finalize()

    # Return IV concatenated with ciphertext
    return iv + ciphertext


def aes_cbc_decrypt(encrypted_msg: bytes, key: bytes) -> bytes:
    """
    Decrypts a message encrypted using AES in CBC mode.
    
    Parameters:
        encrypted_msg (bytes): The encrypted message (IV + ciphertext).
        key (bytes): The decryption key (must be 16, 24, or 32 bytes long).
    
    Returns:
        bytes: The original plaintext message.
    """
    if len(key) not in {16, 24, 32}:
        raise ValueError("Key must be 16, 24, or 32 bytes long.")
    
    # Extract the IV (first 16 bytes) and ciphertext (remaining bytes)
    iv = encrypted_msg[:16]
    ciphertext = encrypted_msg[16:]
    
    # Create the AES cipher in CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the ciphertext
    padded_msg = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding from the decrypted message
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    msg = unpadder.update(padded_msg) + unpadder.finalize()
    
    return msg


def main():
    with open("/home/kon/image-small.jpeg", "rb") as f:
        image = f.read()
    
    key = os.urandom(16)
    encrypted_image = aes_cbc_encrypt(image, key)

    k0n = int(input("What do you want to know? "))
    print(f'{key = }')
    print(f'{encrypted_image[k0n:k0n+32] = }')

if __name__ == "__main__":
    main()