import time
from subprocess32 import run, STDOUT, PIPE, CalledProcessError

print("5 years in prison! Wanna escape???")
payload = input()[:0xc0].encode('utf-8', 'surrogateescape')
st = time.time()

try:
	result = run(['/home/prisonbreak/prisonbreak'], input=payload, stdout=PIPE, stderr=STDOUT, timeout=2, check=True).stdout
except CalledProcessError as e:
	pass

while time.time()-st<5:
	time.sleep(0.001)