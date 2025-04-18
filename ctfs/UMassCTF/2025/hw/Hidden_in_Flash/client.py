from sys import argv
import socket
import time

MAX_SIZE = 64 * 1024
HOST = "hardware.ctf.umasscybersec.org"
PORT = 10003

if len(argv) != 2:
    print(f"Usage: {argv[0]} FIRMWARE_PATH")
    exit(1)

with open(argv[1], 'rb') as f:
    data = f.read()

if len(data) > MAX_SIZE:
    print(f"firmware too large. {len(data)} > {MAX_SIZE}")
    exit(1)

time_err = TimeoutError("Did not receive expected data in time. Please make sure you are submitting an ELF and try again or submit a ticket")

def recv(socket: socket.socket, num_bytes: int, timeout: float = 5) -> bytes:
    output = b''
    start = time.time()
    while num_bytes > 0 and time.time() - start < timeout:
        recvd = socket.recv(num_bytes)
        num_bytes -= len(recvd)
        output += recvd
    if num_bytes:
        raise time_err
    return output

def recv_until(socket: socket.socket, end: bytes, timeout: float = 5) -> bytes:
    output = b''
    start = time.time()
    while time.time() - start < timeout:
        recvd = socket.recv(1)
        if recvd == end:
            return output
        output += recvd
    raise time_err

with socket.socket(socket.AF_INET, socket.SocketKind.SOCK_STREAM) as s:
    print("Connecting...")
    s.connect((HOST, PORT))
    print("Sending firmware...")
    s.sendall(len(data).to_bytes(4, "little") + data)
    if recv(s, 1) != b"\x00":
        print("Unknown response from server")
        exit(1)
       
    print("Running code...")
    rsp_msgs = [
        "Code ran successfully!",
        "Internal error occurred while setting up sim. Please make sure you are uploading an ELF file for the the atmega328p at 16MHz. If the issue persists, submit a ticket.",
        "The sim crashed while running your code. Please make sure your code is built for the atmega328p at 16MHz."
    ]
    ret = int.from_bytes(recv(s, 1))
    if ret < 3:
        print(rsp_msgs[ret])
    else:
        print("Unknown response from server")
    
    data = recv(s, int.from_bytes(recv(s, 4), 'little'))
    print("UART output:")
    try:
        print(data.decode())
    except UnicodeDecodeError:
        print(data)
