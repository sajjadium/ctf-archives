import socket
import random
import threading
from _thread import *
from Crypto.Util.number import long_to_bytes as l2b, bytes_to_long as b2l, getPrime, isPrime, inverse
from math import gcd
from binascii import hexlify, unhexlify

HOST = '0.0.0.0'  # Standard loopback interface address (localhost)
PORT = 60003        # Port to listen on (non-privileged ports are > 1023)
FLAG = open('flag.txt', 'r').read().strip().encode()

def decrypt(flag_ct, ct, d, n):
    pt = 'null'
    if isPrime(ct) and ct != flag_ct:
        pt = hexlify(l2b(pow(ct, d, n))).decode()
    return pt

def gen_params():
    while True:
        p,q = getPrime(1024), getPrime(1024)
        n = p*q
        e = 0x10001
        phi = (p-1)*(q-1)
        if gcd(phi, e) == 1:
            d = inverse(e, phi)
            break
    return n,e,d

def threading(conn):
    n,e,d = gen_params()
    flag_ct = pow(b2l(FLAG), e, n)
    print(f'n: {n}\ne: {e}\nd: {d}')
    conn.sendall(f'n: {hex(n)}\ne: {hex(e)}\nflag_ct: {hex(flag_ct)}\n\n'.encode())
    while True:
        conn.sendall(b'Gimme ct (hex): ')
        try:
            ct = int(conn.recv(1024).strip().decode(), 16)
        except Exception as e:
            conn.sendall(b'invalid ct')
            break
        
        pt = decrypt(flag_ct, ct, d, n)
        conn.sendall(f'result: {pt}\n\n'.encode())

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

