#!/bin/sh

C=FR
O=Donjon
CA_CN=donjon-ctf.io
SERVER_CN=vpn.donjon-ctf.io
SERVER_SAN=vpn.donjon-ctf.io
CLIENT_CN=client@donjon-ctf.io

CA_KEY=caKey.pem
CA_CERT=caCert.pem
SERVER_KEY=serverKey.pem
SERVER_CERT=serverCert.pem
CLIENT_KEY=clientKey.pem
CLIENT_CERT=clientCert.pem

openssl genrsa -3 > $CA_KEY
ipsec pki --self --in $CA_KEY --dn "C=$C, O=$O, CN=$CA_CN" --ca --outform pem > $CA_CERT

openssl genrsa -3 > $SERVER_KEY
ipsec pki --issue --in $SERVER_KEY --type priv --cacert $CA_CERT --cakey $CA_KEY --dn "C=$C, O=$O, CN=$SERVER_CN" --san="$SERVER_SAN" --flag serverAuth --flag ikeIntermediate --outform pem > $SERVER_CERT

openssl genrsa -3 > $CLIENT_KEY
ipsec pki --issue --in $CLIENT_KEY --type priv --cacert $CA_CERT --cakey $CA_KEY --dn "C=$C, O=$O, CN=$CLIENT_CN" --san="$CLIENT_CN" --outform pem > $CLIENT_CERT


