#/bin/sh
./qemu-system-aarch64 \
        -nographic \
        -monitor /dev/null \
        -serial stdio -serial /dev/null\
        -machine virt,secure=on -cpu cortex-a57 -m 1057 -bios  ./bl1.bin \
        -semihosting-config enable,target=native -d unimp \
        -initrd ./rootfs.cpio.gz \
        -kernel ./Image -no-acpi \
        -append 'console=ttyAMA0,38400 keep_bootcon root=/dev/vda2' \
        -boot c
