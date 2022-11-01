'''
entry point. This file manages orders received by clients
and executes the requested commands. For this demo the
commands store,dump and plugin are implemented, though
this version ships without any plugins.
'''

import socket
from threading import Thread
import traceback
from disk import store_disk
from plugin import execute_plugin

ENTRIES = {}

def recv_exact(c,n):
    b = b''
    while len(b) != n:
        b += c.recv(n-len(b))
    return b

def handle_client(con):
    try:
        cmd = recv_exact(con,1).decode()
        assert cmd in ['P','S','D'] , "invalid command received"

        if cmd == 'S': # Store
            entry = recv_exact(con,12)

            data_len = recv_exact(con,1)[0]
            data = recv_exact(con,data_len).decode()

            assert len(list(filter(lambda x : x in '0123456789abcdef',data))) == len(data) , "data has to be in hex format"

            ENTRIES[entry] = bytes.fromhex(data)

            con.send(f'STORED {int(data_len/2)} bytes in {entry}\n'.encode())
        
        if cmd == 'D': # dump to disk
            store_disk(ENTRIES)
            con.send(f'DUMPED {len(ENTRIES)} entries to disk\n'.encode())
        
        if cmd == 'P': # run plugin on data
            plugin_name = recv_exact(con,12).decode()
            try:
                execute_plugin(plugin_name,ENTRIES)
            except Exception as e:
                print(traceback.format_exc())

        con.close()


    except Exception as e:
        con.send(f'{e}'.encode())
        con.close()

def main():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0',4444))
    s.listen(100)

    while True:
        con,addr = s.accept()
        Thread(target=handle_client,args=(con,)).start()

if __name__ == '__main__':
    main()