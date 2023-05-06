from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
import datetime
import os
import config

castle_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>moat</title>
</head>
<body>
<script>
const iframe = document.createElement('iframe');
iframe.sandbox = 'allow-scripts';
iframe.srcdoc = `<script>window.flag = '${new URLSearchParams(window.location.search).get('flag')}'</script\>
<script>${new URLSearchParams(window.location.search).get('eval')}</script\>`;
document.body.appendChild(iframe);
</script>
</body>
</html>"""

def gen_ca():
    private_key = ec.generate_private_key(ec.SECP256R1())
    public_key = private_key.public_key()

    builder = x509.CertificateBuilder()

    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'sndbx'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'sndbx'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'sndbx'),
        x509.NameAttribute(NameOID.COMMON_NAME, 'sndbx'),
    ]))

    builder = builder.issuer_name(x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, 'US'),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, 'sndbx'),
        x509.NameAttribute(NameOID.LOCALITY_NAME, 'sndbx'),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, 'sndbx'),
        x509.NameAttribute(NameOID.COMMON_NAME, 'sndbx'),
    ]))

    builder = builder.not_valid_before(datetime.datetime.today())
    builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(days=365))
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(private_key.public_key())
    builder = builder.add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
    builder = builder.add_extension(x509.SubjectKeyIdentifier.from_public_key(public_key), critical=False)
    builder = builder.add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(public_key), critical=False)
    builder = builder.add_extension(x509.KeyUsage(
        digital_signature=True,
        content_commitment=False,
        key_encipherment=True,
        data_encipherment=False,
        key_agreement=False,
        crl_sign=True,
        encipher_only=False,
        decipher_only=False,
        key_cert_sign=True
    ), critical=True)

    certificate = builder.sign(private_key=private_key, algorithm=hashes.SHA256())

    os.makedirs('ca', exist_ok=True)

    with open('ca/cert.pem', 'wb') as f:
        f.write(certificate.public_bytes(
            encoding=serialization.Encoding.PEM,
        ))

    with open('ca/priv.pem', 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

def gen_cert(domain):
    with open('ca/cert.pem', 'rb') as f:
        ca_cert_pem = f.read()
        ca_cert = x509.load_pem_x509_certificate(ca_cert_pem)

    with open('ca/priv.pem', 'rb') as f:
        ca_private_key = serialization.load_pem_private_key(f.read(), password=None)

    cert_private_key = ec.generate_private_key(ec.SECP256R1())
    cert_public_key = cert_private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, domain)
    ]))
    builder = builder.issuer_name(ca_cert.issuer)
    builder = builder.public_key(cert_public_key)
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(datetime.datetime.today())
    builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(days=90))
    builder = builder.add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName(domain)
        ]),
        critical=False
    )

    # mini-rant: apple is stupid and i spent way too long figuring out why the chall was broken for mac users
    builder = builder.add_extension(
        x509.ExtendedKeyUsage([
            ExtendedKeyUsageOID.SERVER_AUTH
        ]),
        critical=False
    )

    builder = builder.sign(ca_private_key, hashes.SHA256())

    return (
        builder.public_bytes(serialization.Encoding.PEM) + b'\n' + ca_cert_pem,
        cert_private_key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption()
        )
    )

def gen_root():
    os.makedirs('certs/.root', exist_ok=True)

    public_key, private_key = gen_cert(config.DOMAIN)

    with open('certs/.root/cert.pem', 'wb') as f:
        f.write(public_key)

    with open('certs/.root/priv.pem', 'wb') as f:
        f.write(private_key)

def add_castle():
    public_key, private_key = gen_cert(f'castle.{config.DOMAIN}')

    os.makedirs('certs/castle', exist_ok=True)

    with open('certs/castle/cert.pem', 'wb') as f:
        f.write(public_key)

    with open('certs/castle/priv.pem', 'wb') as f:
        f.write(private_key)

    os.makedirs('content', exist_ok=True)

    with open(f'content/castle', 'wb') as f:
        f.write(castle_template.encode())

gen_ca()
gen_root()
add_castle()