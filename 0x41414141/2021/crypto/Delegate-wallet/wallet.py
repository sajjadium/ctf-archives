import os
import socketserver
import string
import threading
from time import *
import time
import binascii
import random

flag = open("flag.txt", "rb").read().strip()

class prng_lcg:

    def __init__(self):
        self.n = pow(2, 607) -1 
        self.c = random.randint(2, self.n)
        self.m = random.randint(2, self.n)
        self.state = random.randint(2, self.n)

    def next(self):
        self.state = (self.state * self.m + self.c) % self.n
        return self.state

class Service(socketserver.BaseRequestHandler):

    def handle(self):
        RNG = prng_lcg()
        while True:
            self.send("1) Generate a new wallet seed")
            self.send("2) Guess the next wallet seed")
            choice = self.receive("> ")
            print(choice)
            if choice == b'1':
                self.send(str(RNG.next()))
            elif choice == b'2':
                guess = int(self.receive("> ").decode())
                if guess == RNG.next():
                    self.send(flag)
                else:
                    self.send("Nope!")

    def send(self, string, newline=True):
        if type(string) is str:
            string = string.encode("utf-8")

        if newline:
            string = string + b"\n"
        self.request.sendall(string)

    def receive(self, prompt="> "):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(
    socketserver.ThreadingMixIn,
    socketserver.TCPServer,
    socketserver.DatagramRequestHandler,
):
    pass


def main():

    port = 4008
    host = "0.0.0.0"

    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True

    server_thread = threading.Thread(target=server.serve_forever)

    server_thread.daemon = True
    server_thread.start()

    print("Server started on " + str(server.server_address) + "!")

    # Now let the main thread just wait...
    while True:
        sleep(10)


if __name__ == "__main__":
    main()