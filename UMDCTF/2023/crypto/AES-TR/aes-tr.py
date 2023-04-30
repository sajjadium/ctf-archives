import socket
import random
import threading
from _thread import *
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l
from Crypto.Util.strxor import strxor
from binascii import hexlify, unhexlify

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 60000        # Port to listen on (non-privileged ports are > 1023)
FLAG = open('flag.txt', 'r').read().strip()
MENU = "\nWhat would you like to do?\n\t(1) Encryption Query\n\t(2) Check Bit\n\t(3) Exit\n\nChoice: "
INITIAL = "Welcome to the best symmetric encryption scheme ever. I'll give you a flag if you can prove this scheme insecure under IND-CPA, but I know it's impossible!! >:)\n"

BS = 16 # Block Size
MS = 30 # Maximum blocks per query
MAX_QUERIES = 10
NUM_BITS = 128

def encrypt(m):
    m = unhexlify(m)
    iv = Random.get_random_bytes(16)
    key = Random.get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)

    blocks = [m[i:i+BS] for i in range(0, len(m), BS)]
    ct = iv
    for i in range(len(blocks)):
        ctr = l2b((b2l(iv)+i+1) % pow(2,BS*8))
        ctr = b'\x00'*(BS - len(ctr)) + ctr # byte padding if ctr < pow(2,BS*8 - 1)
        ct += cipher.encrypt(strxor(ctr, blocks[i]))

    assert len(ct) - len(m) == BS
    return hexlify(ct)
    

def threading(conn):
    conn.sendall(INITIAL.encode())

    for bit in range(NUM_BITS):
        queries = 0
        b = random.randint(0,1)
        while queries < MAX_QUERIES:
            conn.sendall(MENU.encode())
            try:
                choice = conn.recv(1024).decode().strip()
            except ConnectionResetError as cre:
                return

            # ENCRYPTION QUERY
            if choice == '1':
                queries += 1
                conn.sendall(b'm0 (hex): ')
                m0 = conn.recv(1024).strip()
                conn.sendall(b'm1 (hex): ')
                m1 = conn.recv(1024).strip()

                if (len(m0) % 2 != 0) or ((len(m0) // 2) % BS != 0) or ((len(m0) // (2*BS)) > MS):
                    conn.sendall(b'invalid m0\n')
                elif (len(m1) % 2 != 0) or ((len(m1) // 2) % BS != 0) or ((len(m1) // (2*BS)) > MS):
                    conn.sendall(b'invalid m1\n')
                elif len(m0) != len(m1):
                    conn.sendall(b'messages must be same length\n')
                else:
                    if b == 0:
                        ct = encrypt(m0)
                    else:
                        ct = encrypt(m1)
                    conn.sendall(b'ct: ' + ct + b'\n')
                    continue

            # CHECK BIT
            elif choice == '2':
                conn.sendall(b'Bit (b) guess: ')
                b_guess = conn.recv(1024).strip().decode()
                if b_guess == str(b):
                    conn.sendall(b'correct!\n')
                    break
                else:
                    conn.sendall(b'wrong\n')
            
            # EXIT
            elif choice == '3':
                conn.sendall(b'bye homie\n')
            
            # INVALID
            else:
                conn.sendall(b'invalid menu choice\n')

            # close connection on exit, invalid choice, wrong bit guess, invalid encryption query
            conn.close()
            return

        if queries > MAX_QUERIES:
            conn.sendall(f'too many queries: {queries}\n'.encode())
            conn.close()
            return
            
    # Bits guessed correctly
    conn.sendall(f'okay, okay, here is your flag: {FLAG}\n'.encode())
    conn.close()


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            print(f'new connection: {addr}')
            start_new_thread(threading, (conn, ))
        s.close()

