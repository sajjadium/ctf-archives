#!/usr/bin/env python3.8

import random
import requests
import socket
import string
import subprocess
from contextlib import closing


def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def gen_password(len):
    alpha = string.ascii_letters
    return ''.join([random.choice(alpha) for _ in range(len)])

def get_external_ip():
    return requests.get('https://checkip.amazonaws.com').text.strip()

def main():  
    try:
        port = get_free_port()
        admin_pass = gen_password(20)
        connect_pass = gen_password(5)

        proc = subprocess.Popen([
                '/usr/bin/docker',
                'run',
                '-p', f'{port}:28785/udp',  # host:container
                'sauerbraten',
                '-mcr0wn.uk',  # intentionally invalid master server
                f'-p{admin_pass}',
                f'-y{connect_pass}',
                f'-n"pwn me :)"'
            ])
    except Exception as e:
        print(f'Failed to start server: {e}\nPlease report this.')
        exit(1)

    server_ip = '<server IP>'
    try:
        server_ip = get_external_ip()
    except:
        pass

    print(f'Server started on port {port}')
    print(f'Connect in your client with /connect {server_ip} {port} {connect_pass}')
    print(f'This will expire in 5 minutes')

if __name__ == '__main__':
    main()
