from sqlalchemy.exc import OperationalError
from OpenSSL import crypto
import os

with open('secret', 'wb') as f:
    f.write(os.urandom(32))

from app import app, db

run = True
while run:
    try:
        with app.app_context():
            # Init database
            db.create_all()

            # Generate CA certificate
            k = crypto.PKey()
            k.generate_key(crypto.TYPE_RSA, 4096)
            cert = crypto.X509()
            cert.get_subject().C = "DE"
            cert.get_subject().ST = "NRW"
            cert.get_subject().O = "RedRocket"
            cert.get_subject().OU = "Applied Cyberforces"
            cert.get_subject().CN = "Cool CA"
            cert.get_subject().emailAddress = "lol@lol.lol"
            cert.set_serial_number(1337)
            cert.add_extensions([crypto.X509Extension(type_name=b"basicConstraints", critical=True, value=b"CA:TRUE"), crypto.X509Extension(type_name=b"keyUsage", critical=True, value=b"keyCertSign")])
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(10*365*24*60*60)
            cert.set_issuer(cert.get_subject())
            cert.set_pubkey(k)
            cert.sign(k, 'sha512')
            with open('ca.crt', 'wt') as f:
                f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode("utf-8"))
            with open('ca.key', 'wt') as f:
                f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k).decode("utf-8"))

            run = False
    except OperationalError:
        pass  # This will happen if the database is not started
