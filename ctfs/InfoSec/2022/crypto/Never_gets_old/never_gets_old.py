from Crypto.Util.number import bytes_to_long 
from flag import flag
import arrow
import time
import socket
import os
from _thread import *

host = "0.0.0.0"
port = 2022
ServerSideSocket = socket.socket()
ThreadCount = 0

e = 3
n = 56751557236771291682484925205552213395017286856788424728477520869245312923063269575813709372701501266411744107612661617541524170940980758483006610928802060405295040733651568454102696982761234303408607315598889877531472782169525357044937048595117628739355131854220684649309005299064732402206958720387916062449

flag = bytes_to_long(flag.encode())


try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))
print('Socket is listening..')
ServerSideSocket.listen(5)
def multi_threaded_client(connection):
    while True:
        cur_time = int(arrow.utcnow().timestamp())
        m = flag + cur_time
        enc_flag = pow(m,e,n)
        message = str(enc_flag)+"\n"
        connection.sendall(message.encode('utf8'))
        time.sleep(5)
    connection.close()
while True:
    Client, address = ServerSideSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(multi_threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSideSocket.close()