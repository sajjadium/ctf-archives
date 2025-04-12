import random
import socket
import time

random.seed(some_number)

print("Random values:", [random.getrandbits(32) for _ in range(here_too)])

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))
server_socket.listen(5)
print("Server listening on port 12345")

while True:
    conn, addr = server_socket.accept()
    try:
        print(f"Connection from {addr}")
        conn.sendall(b"Guess which number I'm thinking:\n")
    
        while True:
            data = conn.recv(1024)
            if not data:
                break
        
            try:
                guess = int(data.strip())
            except ValueError:
                conn.sendall(b"Invalid input. Send a number.\n")
                continue
        
            correct_number = random.getrandbits(32)
        
            if guess == correct_number:
                conn.sendall(b"Correct! Here is your flag: THC{This_is_not_the_real_flag}\n")
                break
            else:
                conn.sendall(f"Nope! The number was {correct_number}. Try again!\nGuess which number I'm thinking:\n".encode())
    
        conn.close()
    except Exception as e:
        print(f"Error: {e}")
        conn.close()

server_socket.close()
