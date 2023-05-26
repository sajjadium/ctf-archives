#!/bin/sh
openssl genpkey -algorithm RSA -out private.key -pkeyopt rsa_keygen_bits:2048
openssl rsa -pubout -in private.key -out static/public_key.pem
