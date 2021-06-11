We thought the file systems that were out there were too complicated, so we wrote our own! It has all of the basic features you may want and removed everything that is unnecessary (and I mean everything). Time for test it out!

Both files are not required to download!

bootable-rpi0-phys-willow.img -- bootable image complete with rpi boot binaries/kernel, write-ready to sd card, use standard UART pins
kernel-rpi0-qemu-willow.img -- only kernel image ready for QEMU v5, load address differs from physical pi load address

Helpful things:

qemu-system-arm -M raspi0 -kernel $(KERN).img -serial null -serial stdio - run kernel in QEMU v5

When connecting to the netcat server and receive the initial message Press to start..., press enter (rather than another key). Otherwise output could be unpredictable.

BCM2835 datasheet: https://www.alldatasheet.com/datasheet-pdf/pdf/502533/BOARDCOM/BCM2835.html

https://drive.google.com/drive/folders/1rLy2mkshZPBDMqtS0ePqh-vLyCRl3nfg?usp=sharing
