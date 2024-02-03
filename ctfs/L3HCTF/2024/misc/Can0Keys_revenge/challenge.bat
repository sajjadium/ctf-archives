@echo off

set PIN=XXXXXX
set WORKDIR="C:\Program Files\OpenSC Project\OpenSC\tools"

wsl echo "-----flag is-----"
wsl cat flag1.txt flag2.txt flag3.txt
wsl echo "-----------------"

%WORKDIR%\pkcs11-tool -l --pin %PIN% --keypairgen --key-type rsa:2048 --id 1 --label "RSA2K"
%WORKDIR%\pkcs11-tool -l --pin %PIN% --read-object --id 1 --type pubkey > public.der
wsl openssl rsa -inform DER -outform PEM -in public.der -pubin > public.pem
wsl openssl rsautl -encrypt -inkey public.pem -in flag1.txt -pubin -out flag1.txt.enc

%WORKDIR%\pkcs11-tool -l --pin %PIN% --write-object flag2.txt --type data --id 2 --label flag2 --private

%WORKDIR%\pkcs11-tool -l --pin %PIN% --keypairgen --key-type EC:secp384r1 --id 3 --label "EC"
%WORKDIR%\pkcs11-tool -l --pin %PIN% --read-object --id 3 --type pubkey > public.ec
wsl openssl ecparam -genkey -name secp384r1 > client.pem
wsl openssl ec -in client.pem -pubout -outform DER > client.der
%WORKDIR%\pkcs11-tool -l --pin %PIN% --id 3 --derive -i client.der -o share.key
wsl sh -c "openssl enc -aes-256-ecb -in flag3.txt -out flag3.txt.enc -K `md5sum share.key | awk '{print \$1}' | xxd -p -c 999 | head -c 64`"