#!/usr/bin/python3

import subprocess
from threading import Timer
import sys
import os
import tempfile
import secrets
import socket
import functools
import struct

FLAG = b'corctf{test_flag!}'
FILE = 'flag'
ROUNDS = 16
HOST = '0.0.0.0'
PORT = 5000
MAX = 1073741824
TIME = 60

def get_program_output(data):
    print('testing program')
    r = subprocess.Popen(
        ["./wrapper", "./daydream"],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.PIPE,
    )
    timer = Timer(TIME, r.kill)
    try:
        timer.start()
        r.stdin.write(data)
        print('waiting on results')
        r.wait()
    finally:
        timer.cancel()
    return r.stdout.read()


def checker(data):
    try:
        if os.path.exists(FILE):
            os.remove(FILE)

        for i in range(ROUNDS):
            secret = hex(secrets.randbits(128))[2:].encode()
            with open(FILE, 'wb') as f:
                f.write(secret)
            os.chmod(FILE, 0o664)

            output = get_program_output(data)

            os.remove(FILE)

            if output.strip() != secret:
                return False
        return True
    except Exception as e:
        print(f'checker failure {e}')
        return False

def recv_fixed(conn, n):
    data = b''
    while len(data) < n:
        temp = conn.recv(n - len(data))
        if not temp:
            raise Exception(f'did not recieve {n} bytes')
        data += temp
    return data

if __name__ == "__main__":
    print('starting dispatcher service')
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print('received a connection')
                    conn.send(b'zzz....\n')
                    payload_len = struct.unpack('Q', recv_fixed(conn, 8))[0]
                    print(f'expecting {payload_len} bytes')
                    data = recv_fixed(conn, payload_len)
                    result = checker(data)
                    if result:
                        conn.send(b'what a weird dream...\n')
                        conn.send(FLAG + b'\n')
                    else:
                        conn.send(b'failed\n')
        except Exception as e:
            print(f'main handler failure {e}')
            pass
