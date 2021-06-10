#!/usr/bin/env python2

from hashcash import check
import os
import signal
import SocketServer
import threading

magic = os.urandom(8).encode("hex")

class threadedserver(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class incoming(SocketServer.BaseRequestHandler):
    def recvline(self):
        line = ""
        while True:
            read = self.request.recv(1)
            if not read or read == "\n":
                break
            line += read
        return line

    def handle(self):
        resource = os.urandom(8).encode("hex")
        self.request.send(resource)
        self.request.send("\n")
        token = self.recvline()
        if (not check(token, resource=resource, bits=28)) and (not token.startswith(magic)):
            self.request.send("BAD\n")
            self.request.close()
            return

        self.request.send("Welcome to the world's premier search engine\n")
        self.request.send("Enter a URL and a search string, and we'll recursively\n")
        self.request.send("search that page for your given string!\n")
        self.request.send("(eg: https://en.wikipedia.org/wiki/Main_Page Bacon)\n\n")

        pid = os.fork()
        if (pid < 0):
            self.request.send("something super bad happened\n")
            self.request.close()
            return

        if pid:
            self.request.close()
            return

        # reparent to init
        if os.fork():
            os._exit(0)

        os.setsid()
        signal.alarm(30)
        os.dup2(self.request.fileno(), 0)
        os.dup2(self.request.fileno(), 1)
        os.dup2(self.request.fileno(), 2)
        os.execl("./connman", "connman")
        self.request.send("something real bad happened\n")
        self.request.close()


if __name__ == "__main__":
    print "if you want to skip hashcash for debugging: %s" % magic
    SocketServer.TCPServer.allow_reuse_addr = True
    server = threadedserver(('0.0.0.0', 9669), incoming)
    server.timeout = 180
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    server_thread.start()