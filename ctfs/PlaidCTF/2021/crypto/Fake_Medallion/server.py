#!/usr/bin/env python3
import hashcash
import json
import os
import socket
import threading

from carnival import Carnival

HOST = '0.0.0.0'
PORT = 15213

def to_json(dat):
    return json.dumps(dat).encode() + b'\n'

class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen()
        while True:
            client, address = self.sock.accept()
            client.settimeout(90)
            print(f"starting client {address}")
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        carnival = Carnival(address)
        resource = os.urandom(8).hex()
        client.send(resource.encode() + b"\n")
        token = client.recv(64)
        if not hashcash.check(token.decode().strip(), resource, bits=21):
            client.send(b"Bad pow")
            client.close()
            return False
        client.send(carnival.menu())
        while True:
            try:
                data = client.recv(size)
                if data:
                    res = carnival.interact(json.loads(data))
                    if 'help' in res:
                        client.send(res['help'].encode())
                    else:
                        client.send(to_json(res))
                    if 'error' in res:
                        raise Exception("There's an error")
                else:
                    raise Exception('Client disconnected')
            except:
                client.close()
                return False


if __name__ == '__main__':
    Server(HOST, PORT).listen()
