import json
import socketserver
from os import urandom
from random import SystemRandom
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

FLAG ='apoorvctf{!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!}'
BLOCK_SIZE = 16
MAX_QUERIES = 10_000

rng = SystemRandom()

class Challenge:
    def __init__(self):
        self.before_input = "Try to solve me"
        self.secret_message = urandom(BLOCK_SIZE).hex()
        self.encryption_key = urandom(BLOCK_SIZE)
        self.query_count = 0
        self.max_queries = MAX_QUERIES

    def update_query_count(self):
        self.query_count += 1
        if self.query_count >= self.max_queries:
            self.exit = True

    def get_ct(self):
        iv = urandom(BLOCK_SIZE)
        cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv=iv)
        ct = cipher.encrypt(self.secret_message.encode("ascii"))
        return {"ct": (iv + ct).hex()}

    def check_padding(self, ct):
        try:
            ct_bytes = bytes.fromhex(ct)
            iv, ct_body = ct_bytes[:BLOCK_SIZE], ct_bytes[BLOCK_SIZE:]
            cipher = AES.new(self.encryption_key, AES.MODE_CBC, iv=iv)
            pt = cipher.decrypt(ct_body)
            unpad(pt, BLOCK_SIZE)
            is_valid = True
        except (ValueError, Exception):
            is_valid = False
        
        self.update_query_count()
        noisy_response = is_valid ^ (rng.random() > 0.45)
        return {"result": noisy_response}

    def check_message(self, message):
        if message != self.secret_message:
            self.exit = True
            return {"error": "incorrect message"}
        return {"flag": FLAG}

    def challenge(self, msg):
        if "option" not in msg or msg["option"] not in ("encrypt", "unpad", "check"):
            return {"error": "Option must be one of: encrypt, unpad, check"}

        if msg["option"] == "encrypt":
            return self.get_ct()
        elif msg["option"] == "unpad":
            return self.check_padding(msg["ct"])
        elif msg["option"] == "check":
            return self.check_message(msg["message"])


class ChallengeHandler(socketserver.BaseRequestHandler):
    def handle(self):
        chal = Challenge()
        self.request.sendall(chal.before_input.encode() + b'\n')
        
        while not hasattr(chal, 'exit'):
            try:
                data = self.request.recv(4096).decode().strip()
                if not data:
                    break
                
                msg = json.loads(data)
                response = chal.challenge(msg)
                self.request.sendall(json.dumps(response).encode() + b'\n')
                
            except json.JSONDecodeError:
                self.request.sendall(json.dumps({"error": "Invalid JSON"}).encode() + b'\n')
            except Exception:
                break

class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    PORT = 13337
    print(f"Starting server on port {PORT}...")
    with ReusableTCPServer(("0.0.0.0", PORT), ChallengeHandler) as server:
        server.serve_forever()
