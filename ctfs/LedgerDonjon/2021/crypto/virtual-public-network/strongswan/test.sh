#!/bin/sh

sudo charon-cmd --host vpn.donjon-ctf.io --cert caCert.pem --cert clientCert.pem --rsa clientKey.pem --identity client@donjon-ctf.io

