from socket import socket
import socketserver
import argparse
from core import connection_engine, connection_handle_socket
import socket


def banner():
    print('''
     ___  ___  ___ _   _ _ __ ___  ___ ___  _ __  _ __  
    / __|/ _ \/ __| | | | '__/ _ \/ __/ _ \| '_ \| '_ \ 
    \__ \  __/ (__| |_| | | |  __/ (_| (_) | | | | | | |
    |___/\___|\___|\__,_|_|  \___|\___\___/|_| |_|_| |_|
                                                            
    CLIENT
    ''')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--address", required=True,
                        help="remote ip address")
    parser.add_argument(
        "-p", "--port", help="server running port", type=int, required=True)
    parser.add_argument("-d", "--dump", action="store_true", default=False,
                        help="dump payload of packet")
    parser.add_argument("-e", "--encrypt", action="store_true", default=False,
                        help="enable secure encrypted connection")
    args = parser.parse_args()

    HOST, PORT = args.address, args.port

    banner()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((HOST, PORT))

    handler = connection_handle_socket(s, "master", args.dump)
    connection_engine(handler, "master", args.encrypt)
