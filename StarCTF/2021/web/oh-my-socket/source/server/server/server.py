from socket import *
from time import ctime
import time


HOST = '172.21.0.2'
PORT = 21587
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

cnt = 0
while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    cnt += 1
    print('...connnecting from:', addr)

    try:
        while True:
            data = tcpCliSock.recv(BUFSIZ)

            if not data:
                break
            if data == b'*ctf':
                content = open('oh-some-funny-code').read()
                tcpCliSock.send((content.encode()))

            else:
                tcpCliSock.send(('[%s] %s' % (ctime(), data)).encode())
    except Exception as e:
        pass

    if cnt >= 2:
        time.sleep(120)
        tcpSerSock.close()
        exit(0)

tcpSerSock.close()