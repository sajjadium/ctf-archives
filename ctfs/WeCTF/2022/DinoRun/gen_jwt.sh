ssh-keygen -t rsa -b 4096 -m PEM -f private.key
# Don't add passphrase
openssl rsa -in jwtRS256.key -pubout -outform PEM -out public.key
