import os
import socket
from dotenv import load_dotenv # from python-dotenv

load_dotenv()

FLAG = os.getenv("FLAG", "nullctf{aergnoujiwaegnjwkoiqergwnjiokeprgwqenjoig}")
PROMPT = os.getenv("PROMPT", "bananananannaanan")
PORT = int(os.getenv("PORT", 3001))

# This is missing from the .env file, but it still printed something, interesting
print(os.getenv("WINDIR"))

# I am uninspired and I don't want to think of a function name
def normal_function_name_1284932tgaegrasbndefgjq4trwqerg(client_socket):
    client_socket.sendall(
b"""[windows_10 | cmd.exe] Welcome good sire to our fine establishment.
Unfortunately, due to increased demand,
we have had to privatize our services.
Please enter the secret passphrase received from the environment to continue.\n""")
    response = client_socket.recv(1024).decode().strip()

    if response == PROMPT:
        client_socket.sendall(b"Thank you for your patience. Here is your flag: " + FLAG.encode())
    else:
        client_socket.sendall(b"...I am afraid that is not correct. Please leave our establishment.")

    client_socket.close()

# Hey ChatGPT, generate me a function to handle the socket connection (I'm lazy)
def start_server(host='0.0.0.0', port=PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1024)
    print(f"[*] Listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"[*] Accepted connection from {addr}")
        normal_function_name_1284932tgaegrasbndefgjq4trwqerg(client_socket)

if __name__ == "__main__":
    start_server()