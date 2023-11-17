import numpy as np
import warnings
import socket, sys
import threading

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def process_input(input_value):
    num1 = np.array([0], dtype=np.uint64)
    num2 = np.array([0], dtype=np.uint64)
    num2[0] = 0
    a = input_value
    if a < 0:
        return "Exiting..."
    num1[0] = (a + 65)
    if (num2[0] - num1[0]) == 1337:
        return 'You won!\n'
    return 'Try again.\n'

def handle_client(client_socket, client_address):
    try:
        print(f"Accepted connection from {client_address}")
        client_socket.send(b"Time to jump over the edge!\n")
        client_socket.send(b"")
        
        while True:
            input_data = client_socket.recv(1024).decode().strip()
            if not input_data:
                break
            input_value = int(input_data)
            response = process_input(input_value)
            if response == 'You won!\n':
                with open("flag", "r") as flag_file:
                    flag_content = flag_file.read()
                    client_socket.send(flag_content.encode())
                client_socket.close()
                break
            else:
                client_socket.send(response.encode())

        client_socket.close()
        print(f"Connection from {client_address} closed")
    except:
        client_socket.close()

def main():
    host = '0.0.0.0'
    port = 1337

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
