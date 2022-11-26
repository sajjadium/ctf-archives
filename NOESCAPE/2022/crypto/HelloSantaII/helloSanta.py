def enc(msg,key):
	m=""
	i=0
	for char in msg:
		m+=chr(ord(char)+ord(key[i]))
		i+=1
		if(i==len(key)):
			i=0
	return m

def bitEnc(text,key):
	m=""
	for char in text:
		for k in key:
			char = chr(ord(char)+ord(k))
		m+=char
	return m

import io
filename = "helloSanta.txt"
def encryptFile(filename,key):
	file = open(filename,"r")
	filedata= file.read()
	filedata = bitEnc(str(filedata),key)
	file.close()
	with io.open(filename,"w",encoding = "utf-8") as f:
		f.write(filedata)

def readFile(filename):
	with io.open(filename,"r",encoding = "utf-8") as f:
		print(f.read())
readFile(filename)

Key=?????
encryptFile(filename,Key)

readFile(filename)