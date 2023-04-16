import redis
import sys
import socket

host = sys.argv[1]
port = 6379

try:
    r = redis.Redis(host=host, port=port, db=0)
except:
    f = open("/root/redis_error","w")
    f.write("[-] Unable to join redis instance\n")
    f.close()
    exit(-1)

for key in r.keys():
    data = r.get(key)
    #send the data to the php-fpm to send email
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/var/run/php-fpm.sock")
    sock.sendall(data)