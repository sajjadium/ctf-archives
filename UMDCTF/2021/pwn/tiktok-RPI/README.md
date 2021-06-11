This is not what I expected when visiting TikTok! ByteDance decided to put some software on my Raspberry Pi when entering their site, and it wants a password. Can you figure out the password?

Both files are not required to download!

bootable-rpi0-phys-furor.img -- bootable image complete with rpi boot binaries/kernel, write-ready to sd card, use standard UART pins
kernel-rpi0-qemu-furor.img -- only kernel image ready for QEMU v5, load address differs from physical pi load address

Helpful things:

qemu-system-arm -M raspi0 -kernel $(KERN).img -serial null -serial stdio - run kernel in QEMU v5

BCM2835 datasheet: https://www.alldatasheet.com/datasheet-pdf/pdf/502533/BOARDCOM/BCM2835.html

https://drive.google.com/drive/folders/1l3VBDqDtqWqRIEoZJvZTMLEabp48KISt?usp=sharing
