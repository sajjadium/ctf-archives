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
		print('one try every 30 seconds')
		exit(0)
else:
	ips[peerIp] = int(time.time())+30

ipFile.seek(0)
ipFile.write(json.dumps(ips))
ipFile.close()

os.chdir(pathlib.Path(__file__).parent.resolve())

tempdir = tempfile.TemporaryDirectory()
tempdirName = tempdir.name
atexit.register(lambda:tempdir.cleanup())
with open(f'{tempdir.name}/payload.php','wb') as tmp:
	buf = b''
	n = int(input('Length: '))
	if(n > 1024*1024): exit();
	while(len(buf) != n):
		buf += os.read(0,1)
	buf = buf[:n]
	tmp.write(buf)
os.chmod(f'{tempdirName}',0o555)
os.chmod(f'{tempdirName}/payload.php',0o555)
containerName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(0x10))
os.system(f'bash -c "sleep 5 && docker kill {containerName} 2>/dev/null" &')
os.system(f'docker run --name {containerName} --network=none --cpus=1 -m 128mb -v {tempdirName}:/var/www/sbx:ro -v `pwd`/flag.txt:/flag.txt:ro -v `pwd`/php.ini:/etc/php.ini:ro --rm -t php@sha256:2ae8a4334536e4503d6e8c30885bf68dc4b169febaf42a351fdf68ca7aca2b8d php -n -c /etc/php.ini /var/www/sbx/payload.php')


