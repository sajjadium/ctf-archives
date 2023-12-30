#!/usr/bin/env python3
# socat TCP-LISTEN:2323,reuseaddr,fork EXEC:"./deploy.py"
import tempfile
import pathlib
import os
import string
import time
import random
import atexit
import json
import re

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

url = input('input URL (b64ed): ')
if(not re.match('^[A-Za-z0-9=+/]+$',url)):
	print('bad URL')
	exit(1)

os.close(0)
os.close(1)
os.close(2)

containerName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(0x10))
os.system(f'bash -c "sleep 5 && docker kill {containerName} 2>/dev/null" &')
os.system(f'docker run --name {containerName} pupptear bash -c \'/ASIS*/index.js {url}\' ')

