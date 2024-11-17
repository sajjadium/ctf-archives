import os
import socketserver
import json

import x25519
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

HOST_PORT = int(os.environ.get("HOST_PORT", "8000"))
FLAG = os.environ.get("FLAG", "flag{this-is-not-the-real-flag}")
X25519_KEY_SIZE = 32


class Handler(socketserver.BaseRequestHandler):
    timeout = 5.0

    def handle(self):
        request = json.loads(self.request.recv(1024))
        client_pub = bytes.fromhex(request.get("client_pub", ""))
        if len(client_pub) != X25519_KEY_SIZE:
            return

        server_priv = os.urandom(X25519_KEY_SIZE)
        server_pub = x25519.scalar_base_mult(server_priv)
        secret = x25519.scalar_mult(server_priv, client_pub)

        response = {"server_pub": server_pub.hex()}

        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(secret), modes.CTR(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(FLAG.encode()) + encryptor.finalize()

        data = {"iv": iv.hex(), "ct": ct.hex()}

        # This is how you combine dictionaries... right?
        response = response and data

        self.request.sendall(json.dumps(response).encode())


class Server(socketserver.ThreadingTCPServer):
    request_queue_size = 100


def main(host="0.0.0.0", port=HOST_PORT):
    print(f"Running server on {host}:{port}")
    server = Server((host, port), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
