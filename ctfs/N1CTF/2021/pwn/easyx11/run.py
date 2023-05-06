#!/usr/bin/env python3
import socket
import threading
import os
import sys
import ctypes

def send(conn):
    while True:
        try:
            data = conn.recv(4096)
            os.write(sys.stdout.fileno(), data)
        except:
            break
    conn.close()

def recv(conn):
    while True:
        try:
            data = os.read(sys.stdin.fileno(), 4096)
            conn.send(data)
        except:
            break
    conn.close()

def main():
    libc = ctypes.CDLL("libc.so.6")
    libc.alarm(120)
    proxy_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_server.bind(('127.0.0.1', 0))
    proxy_server.listen(50)
    os.popen("DISPLAY=:{} ./x11 2>/dev/null &".format(proxy_server.getsockname()[1] - 6000))
    conn, addr = proxy_server.accept()
    t1 = threading.Thread(target=send, args=(conn, ))
    t2 = threading.Thread(target=recv, args=(conn, ))
    t1.start()
    t2.start()
    try:
        t1.join()
        t2.join()
    except KeyboardInterrupt:
        os._exit(0)
if __name__ == '__main__':
    main()