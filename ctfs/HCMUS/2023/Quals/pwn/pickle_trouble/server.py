import pandas as pd
import io
import time
import threading
import socketserver
import sys
from io import StringIO
import secrets
import os
import numpy as np

FLAG_FILE = "flag.txt"
PORT = int(os.getenv("APP_PORT"))
HOST = "0.0.0.0"

original_stdout = sys.stdout

class Service(socketserver.BaseRequestHandler):
    def handle(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        self.flag = self.get_flag()
        
        token = secrets.token_bytes(16)
        
        self.send(b"Gimme your pickle data size (send as byte string)\n")
        data_size = int(self.request.recv(64).decode())
        
        self.send(b"Gimme your pickle data frame (raw bytes)\n")
        pickle_data = self.receive(data_size)
        df = pd.read_pickle(io.BytesIO(pickle_data))
        
        try:
            if bytes(np.random.choice(df["x"], size=16)) == token:
                print(self.flag)
            else:
                raise Exception("Oh no!")
        except Exception as e:
            print("Oops, you missed it!")
            print(e)
        
        self.send(captured_output.getvalue().encode())
        sys.stdout = original_stdout
        
            
    def get_flag(self):
        with open(FLAG_FILE, 'rb') as f:
            return f.readline()
    
    def send(self, s: str):
        self.request.sendall(s.encode("utf-8"))
        
    def send(self, b: bytes):
        self.request.sendall(b)

    def receive(self, b = 1024):
        data = b""
        while len(data) != b:
            data += self.request.recv(256)
        return data
    
class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass

def main():
    service = Service
    server = ThreadedService((HOST, PORT), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    print("Server started on " + str(server.server_address) + "!")
    # Now let the main thread just wait...
    while True:
        time.sleep(10)
        
if __name__ == "__main__":
    main()
