
import socket
import sys
import time
import struct


def SendCommand(cmd):
	global sock
	
	asBytes = cmd.encode()
	sock.send(len(asBytes).to_bytes(1,"big")+asBytes)
	
	got = sock.recv(1000).decode()
	return got
	
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 1111)
sock.connect(server_address)

print(SendCommand("create,polygon"))

print(SendCommand("addpoint,0,10,10"))

point = SendCommand("getpoint,0,0")

print(point)
p = point[point.find("=")+2:].split(",")
print("Points: %s,%s"%(p[0],p[1]))

SendCommand("print")

sock.close()
