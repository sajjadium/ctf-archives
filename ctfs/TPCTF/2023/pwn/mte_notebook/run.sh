echo "TPCTF{fake_flag_11111111}" > /vm_rootfs/flag1
echo "TPCTF{fake_flag_22222222}" > /vm_rootfs/flag2
cd /vm_rootfs; find . -print0 | cpio --null -ov --format=newc | gzip -9 > /vm_rootfs.cpio.gz; cd -
qemu-system-aarch64 -machine virt,mte=on -cpu max  -kernel /Image -initrd /vm_rootfs.cpio.gz -m 2G -display none -serial stdio -append "root=/dev/mem console=ttyAMA0"