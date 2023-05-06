#! /bin/sh
cd `dirname $0`
mkdir -p cert
openssl req -x509 -nodes -newkey rsa:4096 -keyout cert/cert.pem -out cert/cert.pem -days 365 -subj "/CN=SSLVPN"
chmod 644 cert/cert.pem

openssl genrsa -out cert/ca.key 4096
openssl req -x509 -new -nodes -key cert/ca.key -sha256 -days 365 -out cert/ca.crt -subj "/CN=SSLVPN_CA"

chown 20000:20000 flag.txt
chmod 400 flag.txt
chown 20000:20000 getflag
chmod 555 getflag
chmod +s getflag



