import socket
import subprocess

sock = socket.socket()
sock.bind(('', 5000))
sock.listen(1)

c, _ = sock.accept()

c.send(b'IP: ')
ip = c.recv(1024)
c.send(b'Port: ')
port = c.recv(1024)

subprocess.run(['./nbd-client', ip.strip(), '-N', 'whatever', '-l', port.strip(), '/dev/nbd0'])

c.close()
