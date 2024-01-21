#!/usr/bin/env python3
import tempfile
import pathlib
import os
import re
import json
import time
import signal
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
		ips[peerIp] = int(time.time())+5
	else:
		print('one try every 5 seconds')
		exit(0)
else:
	ips[peerIp] = int(time.time())+5

ipFile.seek(0)
ipFile.write(json.dumps(ips))
ipFile.close()

os.chdir(pathlib.Path(__file__).parent.resolve())
signal.alarm(10)
os.setgid(1000)
os.setuid(1000)

with tempfile.NamedTemporaryFile() as tmp:
	print('Send the file: (ended with "\\n-- EOF --\\n"):')
	s = input()
	while(re.match('^[\x09-\x7f]*$',s) and s != '-- EOF --' and len(s) < 1024*1024):
		tmp.write((s+'\n').encode())
		s = input()
	tmp.flush()
	os.close(0)
	os.system('timeout 3 ./lua ' + tmp.name)
