from tqdm import tqdm # Progress bar :)
from pwn import *     # Import the pwntools module to interact with the server

# Set the host and port
HOST = '???'
PORT = 000
t = remote(HOST, PORT)  # Connect to the server

t.level = 'debug'  # This will print the data sent and received

# Recieve until the challenges start
t.recvlines(2)

for _ in tqdm(range(25)):
    line = t.recvline().decode()   # This returns bytes, so we need to decode it
    action = line.split()[1]
    match action:
        case 'math':
            equation = t.recvuntil(' = ').decode().split(' = ')[0]  # Recieve until the '=' sign and just get the equation
            ...
            
            
        case 'aes':
            line = t.recvline().decode()
            key = line.split()[-1]
            line = t.recvline().decode()
            enc = line.split()[-1]
            ...
            
    res = t.recvline().decode() # Recieve the result of the challenge
        
flag = t.recvline().decode() # If everything went well, the flag is printed
print(flag)
            
            
            
         

