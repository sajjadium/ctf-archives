"!" said the kernel

The challenge is deployed at qdiscworld.flu.xxx.

If you run into trouble with bareudp on Ubuntu, try installing linux-modules-extra for your kernel (typically, this is a recommended dependency of linux-image-generic).

If you run into trouble with bareudp on WSL, try recompiling your kernel with CONFIG_BAREUDP=y or CONFIG_BAREUDP=m. The same advice applies to Debian.

Fedora and ArchLinux should work out of the box.

Product Info
Designer: hlt
