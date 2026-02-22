#!/usr/bin/env python3
import socket
import threading
import random

MODULUS = 1999  # The year 1999 :)
FLAG = "bkctf{test_flag}"

def gcd(a, b):
    """Compute GCD"""
    while b:
        a, b = b, a % b
    return a

def generate_lcg_parameters():
    """Generate random valid LCG parameters"""
    while True:
        a = random.randint(100, MODULUS - 1)
        if gcd(a, MODULUS) == 1:
            break
    c = random.randint(1, MODULUS - 1)
    
    return a, c

class LCG:
    def __init__(self, a, c, seed=None):
        self.a = a
        self.c = c
        if seed is None:
            seed = random.randint(1, MODULUS - 1)
        self.state = seed
    
    def next(self):
        self.state = (self.a * self.state + self.c) % MODULUS
        return self.state

def ascii_art():
    return """
+===============================================================+
|                    Y2K TIME CAPSULE SYSTEM                    |
|                   LOCKED: December 31, 1999                   |
+===============================================================+

[SYSTEM NOTICE] This time capsule is locked behind state of the
art technology. In order to gain access, you must guess correctly
the next 5 access codes in the sequence.
"""

def handle_client(client_socket, address):
    """Handle individual client connection"""
    try:        
        a, c = generate_lcg_parameters()
        
        client_socket.sendall(ascii_art().encode() + b"\n")
        seed = random.randint(1, MODULUS - 1)
        lcg = LCG(a, c, seed)
        
        shown_numbers = [lcg.next() for _ in range(5)]
        answer_numbers = [lcg.next() for _ in range(5)]
        
        client_socket.sendall(b"\nThe last 5 codes used were:\n")
        client_socket.sendall(f"{shown_numbers}\n\n".encode())
        
        client_socket.sendall(b"Predict the NEXT 5 access codes to unlock the bunker!\n")
        client_socket.sendall(b"Enter them as comma-separated values (e.g., 123,456,789,67,420):\n")
        client_socket.sendall(b"> ")
        
        response = client_socket.recv(1024).decode().strip()
        
        try:
            predicted = [int(x.strip()) for x in response.split(',')]
            
            if len(predicted) != 5:
                client_socket.sendall(b"\n[ACCESS DENIED] You must provide exactly 5 codes!\n")
                client_socket.close()
                return
            
            if predicted == answer_numbers:
                client_socket.sendall(b"\n" + b"="*60 + b"\n")
                client_socket.sendall(b"Time Capsule Access Granted!\n")
                client_socket.sendall(b"="*60 + b"\n\n")
                client_socket.sendall(b"Welcome to the Y2K Time Capsule.\n")
                client_socket.sendall(f"Your sensitive contents: {FLAG}\n\n".encode())
            else:
                client_socket.sendall(b"\n[ACCESS DENIED] Incorrect code sequence!\n")
                client_socket.sendall(b"The time capsule remains sealed. Try again!\n")
        
        except ValueError:
            client_socket.sendall(b"\n[ERROR] Invalid format! Use comma-separated numbers.\n")
    
    except Exception as e:
        pass
    
    finally:
        client_socket.close()

def main():
    """Main server function"""
    HOST = '0.0.0.0'
    PORT = 1999
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    
    try:
        while True:
            client_sock, address = server.accept()
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_sock, address)
            )
            client_handler.start()
    except KeyboardInterrupt:
        server.close()

if __name__ == "__main__":
    main()