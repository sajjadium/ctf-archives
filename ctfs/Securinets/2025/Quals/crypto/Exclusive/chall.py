from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os, signal
from secret import FLAG

signal.alarm(30)

class AES_XTS:
    def __init__(self):
        self.key = os.urandom(64)
        self.tweak = os.urandom(16)

    def encrypt(self, plaintext):
        encryptor = Cipher(algorithms.AES(self.key), modes.XTS(self.tweak)).encryptor()
        return encryptor.update(plaintext)

    def decrypt(self, ciphertext):
        decryptor = Cipher(algorithms.AES(self.key), modes.XTS(self.tweak)).decryptor()
        return decryptor.update(ciphertext)


if __name__ == '__main__':
    print("Welcome! Exclusive contents awaits, but you'll have to figure it out yourself.")

    cipher = AES_XTS()

    blocks = [FLAG[i:i+16] for i in range(0, len(FLAG), 16)]

    try:
        print(f"Select a block number to generate a clue (1-{len(blocks)})")
        ind = int(input('> '))
        
        clue = cipher.encrypt(os.urandom(16) + blocks[ind-1])        
        print(f"Your clue : {clue.hex()}")

        while True:
            print("Submit the clue (in hex)")
            your_clue = bytes.fromhex(input('> '))

            decrypted = cipher.decrypt(your_clue)
            decrypted_blocks = [decrypted[i:i+16] for i in range(0, len(decrypted), 16)]

            exclusive_content = decrypted_blocks[0]
            print(f"Exclusive content : {exclusive_content.hex()}")

    except:
        print('Oops! Something went wrong')
