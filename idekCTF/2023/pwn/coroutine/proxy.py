import socket
import sys
import time
import subprocess

proc = subprocess.Popen('./CoroutineCTFChal',stdout=subprocess.PIPE)

line = proc.stdout.readline()
assert line.startswith(b'port number ')
port = int(line[len('port number '):])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    for _ in range(14):
        print('Select Option:')
        print('1. Connect')
        print('2. Change Receive Buffer')
        print('3. Change Send Buffer')
        print('4. Send data')
        print('5. Receive data')

        option = input('> ').strip()
        match option:
            case '1':
                s.connect(('localhost', port))
            case '2':
                size = int(input('Buffer size> ').strip())
                s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, size)
            case '3':
                size = int(input('Buffer size> ').strip())
                s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, size)
            case '4':
                data = input('Data> ').strip()
                s.send(data.encode('utf-8')[:512])
            case '5':
                size = int(input('Size> ').strip())
                print(s.recv(size))
            case _:
                print('Invalid option')
                sys.exit(1)
