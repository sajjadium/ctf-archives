import socket
import threading
from _thread import *
from Crypto.Random import get_random_bytes, random
from binascii import hexlify, unhexlify
import crypto
from wonderwords import RandomWord

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 1234         # Port to listen on (non-privileged ports are > 1023)
FLAG = open('flag.txt', 'r').read().strip()
MENU = "\nWhat would you like to do?\n\t(1) MAC Query\n\t(2) Verification Query\n\t(3) Forgery\n\t(4) Exit\n\nChoice: "
INITIAL = "Can you break my hashed-based MAC again?\n"

MAX_QUERIES = 100
TAGLEN = 20 # SHA1() tag is 20 bytes
INJECTION = b'https://www.youtube.com/@_JohnHammond'

# t = H(key || msg)
def hashed_mac(msg, key):
    h = crypto.Sha1(key + msg)
    t = h.hexdigest()
    return t

# H(key || msg) == tag
def vf_query(conn, key, first_part=None):
    conn.sendall(b'msg (hex): ')
    msg = conn.recv(1024).strip()
    conn.sendall(b'tag (hex): ')
    tag = conn.recv(1024).strip()

    try:
        msg = unhexlify(msg)
        if first_part is not None and (first_part not in msg or INJECTION not in msg):
            conn.sendall(f'forgot something!\n'.encode())
        elif len(tag) != TAGLEN*2: 
            conn.sendall(f'Invalid tag length. Must be {TAGLEN} bytes\n'.encode())
        else:
            t_ret = hashed_mac(msg, key)
            return t_ret.encode() == tag, msg
    except Exception as e:
        conn.sendall(b'Invalid msg format. Must be in hexadecimal\n')
    return False, b''

def mac_query(conn, key):
    conn.sendall(b'msg (hex): ')
    msg = conn.recv(1024).strip()

    try:
        msg = unhexlify(msg)
        t = hashed_mac(msg, key)
        conn.sendall(f'H(key || msg): {t}\n'.encode())
        return msg
    except Exception as e:
        conn.sendall(b'Invalid msg format. Must be in hexadecimal\n') 
    return None

def threading(conn):
    conn.sendall(INITIAL.encode())

    rw = RandomWord()
    first_part = '-'.join(rw.random_words(random.randrange(5,30), word_min_length=5)).encode()
    conn.sendall(f'first_part: {first_part.decode()}\n'.encode())

    key = get_random_bytes(random.randrange(10,120))
    queries = []
    while len(queries) < MAX_QUERIES:
        conn.sendall(MENU.encode())
        try:
            choice = conn.recv(1024).decode().strip()
        except ConnectionResetError as cre:
            return

        # MAC QUERY
        if choice == '1':
            msg = mac_query(conn, key)
            if msg is not None:
                queries.append(msg)

	# VF QUERY
        elif choice == '2':
            res, msg = vf_query(conn, key)
            conn.sendall(str(res).encode())

        # FORGERY 
        elif choice == '3':
            res, msg = vf_query(conn, key, first_part)
            if res and msg not in queries:
                conn.sendall(FLAG.encode() + b'\n')
            elif msg in queries:
                conn.sendall(b"cheater!!!\n")
            else:
                conn.sendall(str(res).encode() + b'\n')
            break

        # EXIT or INVALID CHOICE
        else:
            if choice == '4': 
                conn.sendall(b'bye\n')
            else:
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

