#!/usr/bin/env python3
import socket
import threading
import random
import math

FLAG = "bkctf{test_flag}"

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_prime(n, k=20):
    """Miller-Rabin primality test"""
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1
        if is_prime(n):
            return n

def generate_semiprime():
    while True:
        p = generate_prime(16)
        q = generate_prime(16)
        if p != q:
            return p, q, p * q

def generate_lcg_parameters(modulus):
    while True:
        a = random.randint(modulus // 4, modulus - 1)
        if gcd(a, modulus) == 1:
            break
    while True:
        c = random.randint(modulus // 4, modulus - 1)
        if gcd(c, modulus) == 1:
            break
    return a, c

class LCG:
    def __init__(self, a, c, modulus, seed=None):
        self.a = a
        self.c = c
        self.modulus = modulus
        if seed is None:
            seed = random.randint(1, modulus - 1)
        self.state = seed

    def next(self):
        self.state = (self.a * self.state + self.c) % self.modulus
        return self.state

def ascii_art():
    return """
+===============================================================+
|                    Y2K TIME CAPSULE SYSTEM                    |
|                   LOCKED: December 31, 1999                   |
+===============================================================+

[SYSTEM NOTICE] This time capsule is locked behind state-of-the-
art DUAL-PRIME cryptographic sequencing technology. To gain
access, predict the next 5 access codes in the sequence.
"""

def handle_client(client_socket, address):
    try:
        p, q, modulus = generate_semiprime()
        a, c = generate_lcg_parameters(modulus)
        lcg = LCG(a, c, modulus)

        NUM_SHOWN = 8
        NUM_PREDICT = 5

        shown   = [lcg.next() for _ in range(NUM_SHOWN)]
        answers = [lcg.next() for _ in range(NUM_PREDICT)]

        client_socket.sendall(ascii_art().encode() + b"\n")
        client_socket.sendall(b"The last 8 access codes were:\n")
        client_socket.sendall(f"{shown}\n\n".encode())
        client_socket.sendall(
            b"Predict the NEXT 5 access codes to unlock the bunker!\n"
            b"Enter them as comma-separated values (e.g., 123,456,789,67,420):\n> "
        )

        response = client_socket.recv(1024).decode().strip()

        try:
            predicted = [int(x.strip()) for x in response.split(',')]

            if len(predicted) != NUM_PREDICT:
                client_socket.sendall(
                    f"\n[ACCESS DENIED] Provide exactly {NUM_PREDICT} codes!\n".encode()
                )
                return

            if predicted == answers:
                client_socket.sendall(
                    b"\n" + b"=" * 60 + b"\n"
                    b"Time Capsule Access Granted!\n"
                    + b"=" * 60 + b"\n\n"
                    b"Welcome to the Y2K Time Capsule.\n"
                    + f"Your sensitive contents: {FLAG}\n\n".encode()
                )
            else:
                client_socket.sendall(
                    b"\n[ACCESS DENIED] Incorrect code sequence!\n"
                    b"The time capsule remains sealed. Try again!\n"
                )

        except ValueError:
            client_socket.sendall(b"\n[ERROR] Invalid format! Use comma-separated numbers.\n")

    except Exception:
        pass
    finally:
        client_socket.close()

def main():
    HOST = '0.0.0.0'
    PORT = 1999
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Y2K Time Capsule listening on {HOST}:{PORT}")
    try:
        while True:
            client_sock, address = server.accept()
            threading.Thread(target=handle_client, args=(client_sock, address)).start()
    except KeyboardInterrupt:
        server.close()

if __name__ == "__main__":
    main()