#!/usr/bin/env python3
from flask import Flask,Response,request
import time
import socket
import re
import base64
import json

isSafeAscii = lambda s : not re.search(r'[^\x20-\x7F]',s)
isSafeHeader = lambda s : isSafeAscii(s)
isSafePath = lambda s : s[0] == '/' and isSafeAscii(s) and ' ' not in s
badHeaderNames = ['encoding','type','charset']
unsafeKeywords = ["flag"]

app = Flask(__name__)
application = app

def isJson(s):
	try:
	    json.loads(s)
	    return True
	except:
		return False

def checkHostname(name):
	name = str(name)
	port = '80'
	if(':' in name):
		sp = name.split(':')
		name = sp[0]
		port = sp[1]

	if(
		(
		re.search(r'^[a-z0-9][a-z0-9\-\.]+$',name) or
		re.search(r'^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$',name)
		) and
		0 < int(port) < 0x10000
	):
		return name,int(port)
	return Exception('unsafe port'),Exception('unsafe hostname')

def recvuntil(sock,u):
	r = b''
	while(r[-len(u):] != u):
		r += sock.recv(1)
	return r

def checkHeaders(headers):
	newHeaders = {}
	if(type(headers) is not dict):
		return Exception('unsafe headers') 
	for headerName in headers:
		headerValue = str(headers[headerName])
		if((isSafeHeader(headerName) and ':' not in headerName) and isSafeHeader(headerValue)):
			isBad = False
			for badHeaderName in badHeaderNames:
				if(badHeaderName in headerName.lower()):
					isBad = True
					break
			for badHeaderValue in unsafeKeywords:
				if(badHeaderValue in headerValue.lower()):
					isBad = True
					break
			if(isBad):
				return Exception('bad headers')
			newHeaders[headerName] = headerValue
	return newHeaders

def checkMethod(method):
	if(method in ['GET','POST']):
		return method
	return Exception('unsafe method')

def checkPath(path):
	if(isSafePath(path)):
		return path
	return Exception('unsafe path')

def checkJson(j):
	if(type(j) == str):
		for u in unsafeKeywords:
			if(u in j.lower()):
				return False
	elif(type(j) == list):
		for entry in j:
			if(not checkJson(entry)):
				return False 
	elif(type(j) == dict):
		for entry in j:
			if(not checkJson(j[entry])):
				return False 
	else:
		return True

	return True

@app.route('/req',methods=['POST'])
def req():
	params = request.json

	hostname,port = checkHostname(params['host'])
	headers = checkHeaders(params['headers'])
	method = checkMethod(params['method'])
	path = checkPath(params['path'])
	returnJson = bool(params['returnJson'])
	body = None

	for p in [hostname,headers,body,method,path]:
		if(isinstance(p,Exception)):
			return {'success':False,'error':str(p)}

	if(method == 'POST'):
		body = str(params['body'])


	httpRequest = f'{method} {path} HTTP/1.1\r\n'
	if(port == 80):
		httpRequest+= f'Host: {hostname}\r\n'
	else:
		httpRequest+= f'Host: {hostname}:{port}\r\n'
	httpRequest+= f'Connection: close\r\n'
	if(body):
		httpRequest+= f'Content-Length: {str(len(body))}\r\n'
	for headerName in headers:
		httpRequest+= f'{headerName}: {headers[headerName]}\r\n'
	httpRequest += '\r\n'
	if(body):
		httpRequest += body
	httpRequest = httpRequest.encode()

	with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
		sock.settimeout(1)
		sock.connect((hostname,port))
		sock.sendall(httpRequest)

		statusCode = int(recvuntil(sock,b'\n').split(b' ')[1])
		headers = {}
		line = recvuntil(sock,b'\n').strip()
		while(line):
			headerName = line[:line.index(b':')].strip().decode()
			headerValue = line[line.index(b':')+1:].strip().decode()
			if(isSafeHeader(headerName) and isSafeHeader(headerValue)):
				headers[headerName] = headerValue
			line = recvuntil(sock,b'\n').strip()
		bodyLength = min(int(headers['Content-Length']),0x1000)
		body = b''
		while(len(body) != bodyLength):
			body += sock.recv(1)
		sock.close()

		if(isJson(body.decode())):
			if(not checkJson(json.loads(body.decode()))):
				return {'success':False,'error':'unsafe json'}
			headers['Content-Type'] = 'application/json'
		else:
			headers['Content-Type'] = 'application/octet-stream'

		if(returnJson):
			body = base64.b64encode(body).decode()
			return {'statusCode':statusCode,'headers':headers,'body':body,'req':httpRequest.decode()}

		resp = Response(body)
		resp.status = statusCode

		for headerName in headers:
			for badHeaderName in badHeaderNames:
				if(badHeaderName not in headerName.lower()):
					resp.headers[headerName] = headers[headerName]
		return resp

@app.route('/')
def index():
	resp = Response('hi')
	resp.headers['Content-Type'] = 'text/plain'
	return resp

if(__name__ == '__main__'):
	app.run(port=8000)
