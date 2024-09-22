#!/usr/bin/python3

import os,pwd,re
import socketserver, signal
import subprocess

listen = 3333

blacklist = os.popen("ls /bin").read().split("\n")
blacklist.remove("echo")
#print(blacklist)

def filter_check(command):
    user_input = command
    parsed = command.split()
    #Must begin with echo
    if not "echo" in parsed:
        return False
    else:
        if ">" in parsed:
            #print("HEY! No moving things around.")
            req.sendall(b"HEY! No moving things around.\n\n")
            return False
        else:
            parsed = command.replace("$", " ").replace("(", " ").replace(")", " ").replace("|"," ").replace("&", " ").replace(";"," ").replace("<"," ").replace(">"," ").replace("`"," ").split()
            #print(parsed)
            for i in range(len(parsed)):
                if parsed[i] in blacklist:
                    return False
            return True

def backend(req):
    req.sendall(b'This is shell made to use only the echo command.\n')
    while True:
        #print("\nThis is shell made to use only the echo command.")
        req.sendall(b'Please input command: ')
        user_input = req.recv(4096).strip(b'\n').decode()
        print(user_input)
        #Check input
        if user_input:
            if filter_check(user_input):
                output = os.popen(user_input).read()
                req.sendall((output + '\n').encode())
            else:
                #print("Those commands don't work.")
                req.sendall(b"HEY! I said only echo works.\n\n")
        else:
            #print("Why no command?")
            req.sendall(b"Where\'s the command.\n\n")

class incoming(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(1500)
        req = self.request
        backend(req)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def main():
    uid = pwd.getpwnam('ctf')[2]
    os.setuid(uid)
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", listen), incoming)
    server.serve_forever()

if __name__ == '__main__':
    main()
