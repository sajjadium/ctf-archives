import socket
import base64
from hashlib import md5
from datetime import datetime

host = '0.0.0.0'
port = 9001

class log:
    @staticmethod
    def print(message):
        with open('./decryption_server.log', 'a') as f:
            now = datetime.now()
            f.write(now.strftime("%d/%m/%Y %H:%M:%S") + "\t")
            f.write(message + '\n')    

def decrypt(encrypted):
    key = open('key.txt').read()
    key = key.strip()
    log.print("Key loaded for encrypted message")

    factor = len(encrypted) // len(key) + 1
    key = key * factor
    log.print(f"Key expanded by factor of {factor}")
    key_bytes = key.encode()

    enc_bytes = base64.b64decode(encrypted)
    dec_bytes = bytearray()

    for i in range(len(enc_bytes)):
        dec_bytes.append(enc_bytes[i] ^ key_bytes[i])
        log.print(f"Partial message digest is {md5(dec_bytes).hexdigest()}")
    decrypted = dec_bytes.decode()
    log.print("Message fully decrypted, ready to send...")
    return decrypted

def main_loop():
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    log.print(f"Server listening on host {host} and port {port}")
    
    while True:
        s.listen(1)
        log.print("Listening for connection...")

        c_soc, addr = s.accept()
        log.print(f"Connection received from {addr}")

        ciphertext = c_soc.recv(1024).decode().strip()
        log.print(f"Received encrypted message {ciphertext}")

        plaintext = decrypt(ciphertext)
        c_soc.sendall(plaintext.encode())
        log.print(f"Decrypted message sent!")


if __name__ == '__main__':
    main_loop()