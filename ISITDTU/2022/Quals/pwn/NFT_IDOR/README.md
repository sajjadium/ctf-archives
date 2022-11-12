I heard that people can own NFT, but can we pwn NFT?

Source build instruction:

Clone Linux kernel commit 4fe89d07dcc2804c8b562f6c7896a45643d34b2f (tag v6.0), then revert the commit 95f466d22364a33d183509629d0879885b4f547e.

.config

Compiled kernel on server

Disk image on server

It will have python, vim, nano, build-essential and libnftnl-dev installed so you can build your exploit there. /tmp is writable.

QEMU command line:

qemu-system-x86_64 -m 1024 -hda nft.qcow2 -nographic -smp 2 -kernel bzImage -append "root=/dev/sda ro console=ttyS0"

Login: nft / nft

Note: Please verify your exploit first before attempting on the server, as it's very slow and you will have to wait for POW.

Also please don't DDOS the infrastructure to create a fair competition for others!

nc 34.125.252.51 31337

On the server, the flag will be at /flag.

