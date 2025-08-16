import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import binascii

HOST = "0.0.0.0"
PORT = 9999
key = b'????????????????'
BLOCK_SIZE = 16

def handle_client(conn):
    conn.sendall(b"Welcome to Padding Oracle service!\nSend ciphertext hex and press enter.\n")
    while True:
        try:
            data = conn.recv(1024).strip()
            if not data:
                break
            ciphertext_hex = data.decode()

            try:
                ciphertext = binascii.unhexlify(ciphertext_hex)
                iv = ciphertext[:BLOCK_SIZE]
                ct = ciphertext[BLOCK_SIZE:]
                cipher = AES.new(key, AES.MODE_CBC, iv)
                plaintext = cipher.decrypt(ct)
                unpad(plaintext, BLOCK_SIZE)
                conn.sendall(b"Valid padding\n")
            except Exception:
                conn.sendall(b"Invalid padding\n")
        except Exception:
            break
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Padding Oracle server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"Connection from {addr}")
            handle_client(conn)

if __name__ == "__main__":
    main()