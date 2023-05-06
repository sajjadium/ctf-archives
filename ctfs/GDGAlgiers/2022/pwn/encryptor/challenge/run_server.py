import socketserver
import os
import sys

import encryptor

BUFFER_SIZE = 1024


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    allow_reuse_address = True

    def handle(self):
        self.request.send(
            b"choose an option:\n1) Try our fast AES implementation\n2) Try our fast RC4 implementation\n"
        )
        option = self.request.recv(BUFFER_SIZE).decode().strip()
        if option == "1":
            self.request.send(b"NOT IMPLEMENTED YET ?\n")
        elif option == "2":
            self.request.send(b"Key:\n")
            key = self.request.recv(BUFFER_SIZE)
            self.request.send(b"Data:\n")
            data = self.request.recv(BUFFER_SIZE)
            response = encryptor.rc4(key, data)
            self.request.send(b"Output:\n")
            self.request.sendall(response)
        else:
            self.request.send(b"Invalid option\n")


class ThreadedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 1337

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    print("Server loop running in process:", os.getpid(), file=sys.stderr)
    server.serve_forever()
