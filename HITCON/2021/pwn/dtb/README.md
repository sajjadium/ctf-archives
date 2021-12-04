# DTB

```
$ git submodule status
 a2547651bc896f95a3680a6a0a27401e7c7a1080 linux (v5.15.6)
```
```
$ make ARCH=arm64 LLVM=1 CROSS_COMPILE=aarch64-linux-gnu- defconfig
$ make ARCH=arm64 LLVM=1 CROSS_COMPILE=aarch64-linux-gnu-
$ file arch/arm64/boot/Image.gz
```

```
$ qemu-system-aarch64 --version
QEMU emulator version 5.2.0 (Debian 1:5.2+dfsg-9ubuntu3.2)
Copyright (c) 2003-2020 Fabrice Bellard and the QEMU Project developers
```

Check run.sh, "example.dtb" will be replaced by the file you upload.
