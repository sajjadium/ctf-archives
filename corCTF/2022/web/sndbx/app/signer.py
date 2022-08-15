import datetime

from cryptography import x509
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

with open('ca/cert.pem', 'rb') as f:
	ca_pem = f.read()
	ca = x509.load_pem_x509_certificate(ca_pem)
 
with open('ca/priv.pem', 'rb') as f:
	private_key = serialization.load_pem_private_key(f.read(), password=None)

def generate(csr):
	cert = x509.CertificateBuilder()
	cert = cert.subject_name(csr.subject)
	cert = cert.issuer_name(ca.issuer)
	cert = cert.public_key(csr.public_key())
	cert = cert.serial_number(x509.random_serial_number())
	cert = cert.not_valid_before(datetime.datetime.today())
	cert = cert.not_valid_after(datetime.datetime(2030, 1, 1))

	for extension in csr.extensions:
		cert = cert.add_extension(extension.value, extension.critical)

	return cert.sign(private_key, hashes.SHA256())
