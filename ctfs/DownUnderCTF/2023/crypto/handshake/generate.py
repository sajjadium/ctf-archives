from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

def get_signed_certificate(subject_name, pubkey, ca_privkey):
    signer = DSS.new(ca_privkey, 'fips-186-3')
    tbs = f'SUBJECT={subject_name}\n{pubkey.export_key(format="PEM")}'
    signature = signer.sign(SHA256.new(tbs.encode()))
    cert = f'{tbs}\n{signature.hex()}'
    return cert

ca_privkey = ECC.generate(curve='p256')
server_privkey = ECC.generate(curve='p256')
admin_privkey = ECC.generate(curve='p256')
you_privkey = ECC.generate(curve='p256')

open('public/ca-pubkey.pem', 'w').write(ca_privkey.public_key().export_key(format='PEM'))
open('private/server-privkey.pem', 'w').write(server_privkey.export_key(format='PEM'))
open('public/server-pubkey.pem', 'w').write(server_privkey.public_key().export_key(format='PEM'))
open('public/you-privkey.pem', 'w').write(you_privkey.export_key(format='PEM'))

you_crt = get_signed_certificate('you', you_privkey.public_key(), ca_privkey)
admin_crt = get_signed_certificate('admin', admin_privkey.public_key(), ca_privkey)
open('public/you.cert', 'w').write(you_crt)
open('public/admin.cert', 'w').write(admin_crt)
