#!/bin/bash

set -e

echo "Building client"

cd client
clang client.c -o client 
cd ..

echo "Building service"
cd sandbox_share_service
clang sandbox_share_xpc.m -o sandbox_share_xpc

echo "Signing service"
codesign -s - -f sandbox_share_xpc
cd ..

echo "Copying service and client"
if [ ! -d "/usr/local/bin" ]; then
	echo "Creating /usr/local/bin, this requires sudo access"
	echo "Please enter your password if prompted"
	sudo mkdir /usr/local/bin
	sudo chown -R `id -u`:`id -g` /usr/local/bin
fi

cp client/client /usr/local/bin/sandbox_share_client
cp sandbox_share_service/sandbox_share_xpc /usr/local/bin/sandbox_share_xpc

echo "Copying sandbox profiles"
if [ ! -d "/usr/local/share" ]; then
	echo "Creating /usr/local/share, this requires sudo access"
	echo "Please enter your password if prompted"
	sudo mkdir /usr/local/share
	sudo chown -R `id -u`:`id -g` /usr/local/share
fi

cp sandbox/sandbox_share.sb /usr/local/share/sandbox_share.sb
cp sandbox/client.sb /usr/local/share/sandbox_share_client.sb
cp sandbox/exploit.sb /usr/local/share/sandbox_share_exploit.sb

echo "Copying service plist, this requires sudo access"
echo "Please enter your password if prompted"

sudo cp sandbox_share_service/com.alles.sandbox_share.plist /Library/LaunchDaemons/com.alles.sandbox_share.plist
sudo chown root:wheel /Library/LaunchDaemons/com.alles.sandbox_share.plist
sudo chmod 544 /Library/LaunchDaemons/com.alles.sandbox_share.plist

echo "Creating flag, this requires sudo access"
echo "Please enter your password if prompted"
echo "ALLES!{Not_the_real_flag}" | sudo tee /etc/flag | true
sudo chmod a+r /etc/flag

echo "Done. Please run 'run.sh' now"
