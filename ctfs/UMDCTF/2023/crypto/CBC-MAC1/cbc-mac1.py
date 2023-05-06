import socket
import threading
from _thread import *
from Crypto import Random
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 60001        # Port to listen on (non-privileged ports are > 1023)
FLAG = open('flag.txt', 'r').read().strip()
MENU = "\nWhat would you like to do?\n\t(1) MAC Query\n\t(2) Forgery\n\t(3) Exit\n\nChoice: "
INITIAL = "Team Rocket told me CBC-MAC with arbitrary-length messages is safe from forgery. If you manage to forge a message you haven't queried using my oracle, I'll give you something in return.\n"

BS = 16 # Block Size
MAX_QUERIES = 10
   
def cbc_mac(msg, key):
    iv = b'\x00'*BS
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    t = cipher.encrypt(msg)[-16:]
    return hexlify(t)

def threading(conn):
    conn.sendall(INITIAL.encode())

    key = Random.get_random_bytes(16)
    queries = []
    while len(queries) < MAX_QUERIES:
        conn.sendall(MENU.encode())
        try:
            choice = conn.recv(1024).decode().strip()
        except ConnectionResetError as cre:
            return

        # MAC QUERY
        if choice == '1':
            conn.sendall(b'msg (hex): ')
            msg = conn.recv(1024).strip()

            try:
                msg = unhexlify(msg)
                if (len(msg) + BS) % BS != 0:
                    conn.sendall(f'Invalid msg length. Must be a multiple of BS={BS}\n'.encode())
                else:
                    queries.append(msg)
                    t = cbc_mac(msg, key)
                    conn.sendall(f'CBC-MAC(msg): {t.decode()}\n'.encode())
            except Exception as e:
                conn.sendall(b'Invalid msg format. Must be in hexadecimal\n')

        # FORGERY (impossible as I'm told)
        elif choice == '2':
            conn.sendall(b'msg (hex): ')
            msg = conn.recv(1024).strip()
            conn.sendall(b'tag (hex): ')
            tag = conn.recv(1024).strip()

            try:
                msg = unhexlify(msg)
                if (len(msg) + BS) % BS != 0:
                    conn.sendall(f'Invalid msg length. Must be a multiple of BS={BS} bytes\n'.encode())
                elif len(tag) != BS*2:
                    conn.sendall(f'Invalid tag length. Must be {BS} bytes\n'.encode())
                elif msg in queries:
                    conn.sendall(f'cheater\n'.encode())
                else:
                    t_ret = cbc_mac(msg, key)
                    if t_ret == tag:
                        conn.sendall(f'If you reach this point, I guess we need to find a better MAC (and not trust TR). {FLAG}\n'.encode())
                    else:
                        conn.sendall(str(t_ret == tag).encode() + b'\n')
            except Exception as e:
                conn.sendall(b'Invalid msg format. Must be in hexadecimal\n')

        else:
            if choice == '3': # EXIT
                conn.sendall(b'bye\n')
            else: # INVALID CHOICE
                conn.sendall(b'invalid menu choice\n')
            break


    if len(queries) > MAX_QUERIES:
        conn.sendall(f'too many queries: {len(queries)}\n'.encode())
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

