import socketserver
import threading
import sys
import hashlib
import string
import random
import socket
import subprocess
import requests
import os
import time
import json
from termcolor import colored

HOST, PORT = "0.0.0.0", 9999

SHOST, SPORT = XXX, XXX

NUMBER = 4
POW_DIFFICULTY = 21 
TIMEOUT = 60 * 5
POST_TIMEOUT = 60 * 4
SECRET = os.getenv("SERVER_SECRET")

log_lock = threading.Lock()
bot_lock = threading.Lock()

banner = colored('''
  /$$$$$$     /$$         /$$      /$$
 /$$__  $$   | $$        | $$$    /$$$
| $$  \__/   | $$        | $$$$  /$$$$
|  $$$$$$    | $$        | $$ $$/$$ $$
 \____  $$   | $$        | $$  $$$| $$
 /$$  \ $$   | $$        | $$\  $ | $$
|  $$$$$$/   | $$$$$$$$  | $$ \/  | $$
 \______/    |________/  |__/     |__/
''', 'red')

def log_wrapper(s):
    log_lock.acquire()
    print(colored(f"log - {s}", "yellow"))
    sys.stdout.flush()
    log_lock.release()


def pow(request):
    candidates = string.hexdigits + string.ascii_letters
    prefix = ''
    for _ in range(4):
        prefix += candidates[random.randint(0, len(candidates) - 1)]
    request.sendall(
        "Proof-of-Work, the resource is quite limited hence the pow is somehow difficult XD\n"
        f"sha256({ prefix } + ???).binary.startswith('{ '0' * POW_DIFFICULTY }')\n"
        .encode())
    request.sendall(b"> your ???: ")
    answer = request.recv(256).decode().strip()
    h = hashlib.sha256()
    h.update((prefix + answer).encode())
    bits = "".join(bin(i)[2:].zfill(8) for i in h.digest())
    log_wrapper(f"calculate bits {bits}")
    return bits.startswith("0" * POW_DIFFICULTY)


class SLMTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(TIMEOUT)
        try:
            if not pow(self.request):
                self.request.sendall(b"failed pow ... try again\n")
                self.request.close()
                return

            # actual service here
            self.request.send(banner.encode())
            self.request.send(b"\n")
            self.request.send("I'm a math question bot powered by langchain + RWKV 🤖️\n".encode())
            self.request.send(b"\n")
            self.request.send(b"For example, you can ask me:\n")
            self.request.send(b"Olivia has $23. She bought five bagels for $3 each. ")
            self.request.send(b"How much money does she have left?\n")
            self.request.send(b"\n")
            self.request.send(colored("------------------------------- Your Question -------------------------------\n", "red").encode())
            self.request.send(b"> ")
            
            question_bytes = self.request.recv(256)
            
            for q in question_bytes:
                if chr(q) not in string.printable:
                    self.request.send(b"> ")
                    self.request.send(b"! bad question !")
                    return
            
            question_str = question_bytes.decode().strip()

            log_wrapper(f"receive {question_str}")
            start_time = time.time()

            server_url = f"http://{SHOST}:{SPORT}/api/lsm"
            r = requests.post(server_url, json={"secret": SECRET, "question": question_str}, timeout=POST_TIMEOUT)
            if r.status_code != 200:
                self.request.send(b"> ")
                self.request.send(b"! internal error !")
                return

            reply_json = json.loads(r.text)
            answer = reply_json["result"]

            end_time = time.time()
            cost_time = int(end_time - start_time)
            self.request.send(colored("------------------------------- Your Answer ---------------------------------\n", "red").encode())
            self.request.send(b"\n")
            self.request.send(f"-->\tafter {cost_time} seconds\n".encode())
            self.request.send(f"-->\tyour answer: {answer}\n".encode())
            self.request.send(b"\n")

        except socket.timeout:
            log_wrapper("Connection timed out")
        except Exception as e:
            log_wrapper(f"An error occurred: {e}")

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), SLMTCPHandler) as server:
        server.serve_forever()