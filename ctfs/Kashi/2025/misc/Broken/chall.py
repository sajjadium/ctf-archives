#!/usr/bin/env python3

import hashlib
import socket
import signal
import sys

HOST = "0.0.0.0"
PORT = 1337
SECRET_KEY = b"REDACTED"

def generate_hmac(message):
    return hashlib.sha1(SECRET_KEY + message.encode()).hexdigest()

def signal_handler(sig, frame):
    print("\n[!] Server shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def handle_client(client, addr):
    print(f"[*] Connection from {addr}")

    try:
        original_data = "count=10&lat=37.351&user_id=1&long=-119.827&file=random.txt"
        original_hmac = generate_hmac(original_data)

        client.sendall(f"Retrieve file using format: data|hmac\nExample: {original_data}|{original_hmac}\n".encode())

        data = client.recv(1024)
        if not data:
            print(f"[-] Client {addr} disconnected.")
            return

        try:
            decoded_data = data.decode("utf-8").strip()
        except UnicodeDecodeError:
            decoded_data = data.decode("latin-1").strip()

        print(f"[*] Received Data: {decoded_data}")

        if "|" not in decoded_data:
            client.sendall(b"Invalid format. Use data|hmac\n")
            return

        user_data, received_hmac = decoded_data.rsplit("|", 1)

        user_data_bytes = bytes(user_data, "utf-8").decode("unicode_escape").encode("latin-1")

        h = hashlib.sha1()
        h.update(SECRET_KEY + user_data_bytes)
        computed_signature = h.hexdigest()

        print(f"[*] Computed Signature: {computed_signature} for body: {repr(user_data)}")
        print(f"[*] Received Signature: {received_hmac}")

        if computed_signature != received_hmac:
            client.sendall(b"Invalid HMAC. Try again.\n")
        else:
            try:
                params = dict(param.split("=") for param in user_data.split("&") if "=" in param)
                filename = params.get("file")
                if filename:
                    with open(filename, "r") as f:
                        content = f.read()
                    client.sendall(f"File Contents:\n{content}\n".encode())
                else:
                    client.sendall(b"Invalid request format.\n")
            except FileNotFoundError:
                client.sendall(b"File not found.\n")

    except ConnectionResetError:
        print(f"[!] Client {addr} forcibly disconnected.")

    except Exception as e:
        print(f"[!] Error handling client {addr}: {e}")

    finally:
        client.close()
        print(f"[-] Closed connection with {addr}")

def start_server():
    print(f"[*] Listening on {HOST}:{PORT} ...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    while True:
        try:
            client, addr = server.accept()
            handle_client(client, addr)
        except KeyboardInterrupt:
            print("\n[!] Shutting down server...")
            server.close()
            sys.exit(0)

if __name__ == "__main__":
    start_server()
