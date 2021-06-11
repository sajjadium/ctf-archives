Raspberry Pi Zero baremetal programming is fun! No standard libs, no rules, pure chaos.

Both files are not required to download!

bootable-rpi0-phys-willow.img -- bootable image complete with rpi boot binaries/kernel, write-ready to sd card, use standard UART pins
kernel-rpi0-qemu-willow.img -- only kernel image ready for QEMU v5, load address differs from physical pi load address

Helpful things:

qemu-system-arm -M raspi0 -kernel $(KERN).img -serial null -serial stdio - run kernel in QEMU v5

BCM2835 datasheet: https://www.alldatasheet.com/datasheet-pdf/pdf/502533/BOARDCOM/BCM2835.html

https://drive.google.com/drive/folders/1mfuMg7Bf5nSPPK81k39y2c1ts9hp4BME?usp=sharing
