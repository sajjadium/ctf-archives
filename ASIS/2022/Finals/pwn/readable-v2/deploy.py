#!/usr/bin/env python3
# socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"./deploy.py"
import tempfile
import pathlib
import os
import string
import time
import random
import json

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
		ips[peerIp] = int(time.time())+30
	else:
		print('one try each 30 seconds')
		exit(0)
else:
	ips[peerIp] = int(time.time())+30

ipFile.seek(0)
ipFile.write(json.dumps(ips))
ipFile.close()

os.chdir(pathlib.Path(__file__).parent.resolve())

fname = None
with tempfile.NamedTemporaryFile(delete=False) as tmp:
	fname = tmp.name
	print('1. shell')
	print('2. custom binary')
	if(int(input('> ')) == 1):
		f = open('/bin/bash','rb')
		tmp.write(f.read())
		f.close()
	else:
		buf = b''
		n = int(input('Length: '))
		while(len(buf) != n):
			buf += os.read(0,0x1000)
		buf = buf[:n]

		tmp.write(buf)
		tmp.close()

os.chmod(fname,0o555)
containerName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(0x10))
os.system(f'bash -c "sleep 5 && docker kill {containerName} 2>/dev/null" &')
os.system(f'docker run --name {containerName} --privileged --network=none -i --rm -v {fname}:/tmp/exploit readable_v2')
