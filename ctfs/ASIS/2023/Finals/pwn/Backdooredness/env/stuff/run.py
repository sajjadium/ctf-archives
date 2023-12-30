#!/usr/bin/env python3
import tempfile
import pathlib
import os
import re
import json
import time

if not os.path.exists('/tmp/ips.json'):
	f = open('/tmp/ips.json','w')
	f.write('{}')
	f.close()

ipFile = open('/tmp/ips.json','r+')
peerIp = os.environ['SOCAT_PEERADDR']
ips = {}

ips = json.loads(ipFile.read())
if(peerIp in ips):
	if(time.time() > ips[peerIp]):
		ips[peerIp] = int(time.time())+5
	else:
		print('one try every 5 seconds')
		exit(0)
else:
	ips[peerIp] = int(time.time())+5

ipFile.seek(0)
ipFile.write(json.dumps(ips))
ipFile.close()

os.system('chmod 000 /proc/')

os.setgid(1000)
os.setuid(1000)

os.chdir(pathlib.Path(__file__).parent.resolve())
with tempfile.NamedTemporaryFile() as tmp:
	print('Send your hex-encoded ROM:')
	tmp.write(bytes.fromhex(input()))
	tmp.flush()
	os.close(0)
	os.system('timeout 3 xvfb-run -a ./libs/ld-linux-x86-64.so.2 --library-path ./libs ./SimpleNES ' + tmp.name)
