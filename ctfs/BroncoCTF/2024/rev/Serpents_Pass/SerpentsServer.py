import sys
import errno
import socket
import threading
import math
from functools import lru_cache


def getLine(data: bytes) -> str:
    inpData = data[0:data.index(b'\n')]
    return str(inpData)[2:-1]  # filter out the b''


def gate1():
    return pow(10 * 9 + 7 - 2, 2)


def is_square(num: int) -> bool:
    int_sqrt = lambda x: int(math.sqrt(num))
    return pow(int_sqrt(num), 2) == num


def gate2(guess: int) -> bool:
    if guess > 20:
        return False
    binString = '0'
    for _ in range(0, guess):
        binString += '1'
    binary = int(binString, 2)
    return chr(binary) == '?'


@lru_cache()
def mystery(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return mystery(n - 1) + mystery(n - 2)


def gate3(guess: int) -> bool:
    return is_square(mystery(guess))


def handleConnection(conn, addr) -> bool:
    print('handling connection')
    try:
        with conn:
            print('Connected by', addr)
            conn.sendall(b"You approach The Serpent's Pass. The monster will let you through if you can answer three questions.\n")
            conn.sendall(b"Question 1: What number is the Serpent thinking of?\n")
            data = conn.recv(128)
            if not data:
                return False
            guess1 = int(getLine(data))
            if guess1 == gate1():
                conn.sendall(b'The Serpent is surprised, but continues on with his questions.\n')
                conn.sendall(b"Question 2: What is the Serpent's favorite number?\n")
                data = conn.recv(128)
                if not data:
                    return False
                guess2 = int(getLine(data))
                if gate2(guess2):
                    conn.sendall(b"You now have the Serpent's full attention. It stares at you with its beady eyes. It asks you one last question:\n")
                    conn.sendall(b"Question 3: What is the Serpent's least favorite number?\n")
                    data = conn.recv(128)
                    if not data:
                        return False
                    guess3 = int(getLine(data))
                    if gate3(guess3) == 1:
                        conn.sendall(b'The Serpent bows its head in defeat and slinks off. You run to the other side of the pass and retrieve your flag.\n')
                        conn.sendall(b'The flag has an inscription on it. It reads:\n')
                        try:
                            with open('flag.txt', 'r') as f:
                                flag = f.read()
                        except FileNotFoundError:
                            conn.sendall(b"Flag file not found. If you're seeing this, contact an admin ASAP.\n")
                            return True
                        conn.sendall(bytes(flag + '\n', 'utf-8'))
                        conn.close()
                        return True
                    elif gate3(guess3) == 0:
                        conn.sendall(b'As soon as you answer, the monster lashes back and throws you across the pond. Better luck next time.\n')
                        conn.close()
                        return True
                    else:
                        conn.sendall(b'The Serpent tries to think about your answer, but realizes that it takes too much of his (quite small) brainpower. He throws you across the pond anyway. Try a smaller guess next time.\n')
                        conn.close()
                        return True
                else:
                    conn.sendall(b'As soon as you answer, the monster lashes back and throws you across the pond. Better luck next time.\n')
                    conn.close()
                    return True
            else:
                conn.sendall(b'As soon as you answer, the monster lashes back and throws you across the pond. Better luck next time.\n')
                conn.close()
                return True

    except ConnectionResetError:
        print(f'Connection reset. Connection by {addr} closing...')


def connect(s):
    try:
        print('connected')
        while True:
            try:
                conn, addr = s.accept()
            except ConnectionAbortedError:
                print(f'Client disconnected')
                return

            thread = threading.Thread(target=handleConnection, args=(conn, addr))
            thread.start()
            print(f'# active threads: {threading.active_count()}')

    except KeyboardInterrupt:
        s.close()
        print('exiting...')
        sys.exit(130)


def bind() -> bool:
    HOST = '0.0.0.0'
    PORT = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f'Listening on {PORT}')
        connect(s)
        s.close()
    return False


def main():
    try:
        bind()
    except OSError as error:
        if error.errno == errno.EBADF:
            print(error)
            print('continuing...')


if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print('exiting...')
            sys.exit(130)