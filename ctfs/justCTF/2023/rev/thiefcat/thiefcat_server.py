import socket

HOST = "127.0.0.1"
PORT = 12345

welcome = b'''Welcome to jCTF RE adventure!

Session ID: c7b883235162dde58d4bd7bd1949d184''' + b'\x00' * 16340

lore = b'''You are in a forest holding a flag.

Suddenly a thunderstorm comes around...

Running away to the city, you drop the flag (flag.txt).

The weather clears up...

You try to go back and find the flag, but in the place where you think you dropped flag all you can find is a note with an illegible signature:
"I'll be taking the flag."

~~ Prologue over, closing connection. ~~

// Your adventure to get the flag back starts now.'''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()
conn, addr = s.accept()
conn.sendall(welcome)
print(conn.recv(1024))  # Expected reply: b'K\xb9\xa5\x19\x9b\x18y\xdc\xad\xb0\x112I\x01\tJ\xed\xa7N\x0c\x95{\x0b$\x97J\xb0\\p\n\xf5\xaf'
conn.sendall(lore)