import os

from cryptography.hazmat.primitives import serialization
from glob import glob

subdomains = set()

with open('ca/cert.pem', 'rb') as f:
	ca_cert = f.read()

with open('ca/priv.pem', 'rb') as f:
	ca_priv = f.read()

def add(subdomain, public, private, content=b''):
	try:
		os.mkdir(f'certs/{subdomain}/')
	except:
		return

	with open(f'certs/{subdomain}/cert.pem', 'wb') as f:
		f.write(public.public_bytes(serialization.Encoding.PEM) + b'\n' + ca_cert)

	with open(f'certs/{subdomain}/priv.pem', 'wb') as f:
		f.write(private.private_bytes(
			serialization.Encoding.PEM,
			serialization.PrivateFormat.PKCS8,
			serialization.NoEncryption()
		))

	with open(f'content/{subdomain}', 'wb') as f:
		f.write(content)

	subdomains.add(subdomain)

for subdomain in glob('certs/*'):
	subdomains.add(os.path.basename(subdomain))
